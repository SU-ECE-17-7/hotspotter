# LICENCE
from __future__ import print_function, division
# Python
import sys
from itertools import izip
from itertools import product as iprod
import functools
# Science
import cv2
import numpy as np
from numpy import array, sqrt
# VTool
import vtool.histogram as htool
import vtool.keypoint as ktool
import vtool.linalg as ltool
import vtool.image as gtool


# Command line switch
sys.argv.append('--vecfield')


np.tau = 2 * np.pi  # tauday.com


def patch_gradient(patch, ksize=1, gaussian_weighted=True):
    patch_ = array(patch, dtype=np.float64)
    gradx = cv2.Sobel(patch_, cv2.CV_64F, 1, 0, ksize=ksize)
    grady = cv2.Sobel(patch_, cv2.CV_64F, 0, 1, ksize=ksize)
    if gaussian_weighted:
        gausspatch = gaussian_patch(shape=gradx.shape)
        gradx *= gausspatch
        grady *= gausspatch
    return gradx, grady


def patch_mag(gradx, grady):
    return np.sqrt((gradx ** 2) + (grady ** 2))


def patch_ori(gradx, grady):
    'returns patch orientation relative to the x-axis'
    gori = np.arctan2(grady, gradx)  # outputs from -pi to pi
    gori[gori < 0] = gori[gori < 0] + np.tau  # map to 0 to tau (keep coords)
    gori = gori % np.tau
    return gori


from hscom import tools


@tools.lru_cache()
def gaussian_patch(width=3, height=3, shape=(7, 7), sigma=None, norm_01=True):
    # Build a list of x and y coordinates
    half_width  = width  / 2.0
    half_height = height / 2.0
    gauss_xs = np.linspace(-half_width,  half_width,  shape[0])
    gauss_ys = np.linspace(-half_height, half_height, shape[1])
    # Iterate over the cartesian coordinate product and get pdf values
    gauss_xys  = iprod(gauss_xs, gauss_ys)
    gauss_func = functools.partial(ltool.gauss2d_pdf, sigma=sigma, mu=None)
    gaussvals  = [gauss_func(x, y) for (x, y) in gauss_xys]
    # Reshape pdf values into a 2D image
    gausspatch = np.array(gaussvals, dtype=np.float32).reshape(shape).T
    if norm_01:
        # normalize if requested
        gausspatch -= gausspatch.min()
        gausspatch /= gausspatch.max()
    return gausspatch


def get_unwarped_patches(rchip, kpts):
    'Returns cropped unwarped patch around a keypoint'
    _xs, _ys = ktool.get_xys(kpts)
    xyexnts = ktool.get_xy_axis_extents(kpts=kpts)
    patches = []
    subkpts = []

    for (kp, x, y, (sfx, sfy)) in izip(kpts, _xs, _ys, xyexnts):
        radius_x = sfx * 1.5
        radius_y = sfy * 1.5
        (chip_h, chip_w) = rchip.shape[0:2]
        # Get integer grid coordinates to crop at
        ix1, ix2, xm = htool.subbin_bounds(x, radius_x, 0, chip_w)
        iy1, iy2, ym = htool.subbin_bounds(y, radius_y, 0, chip_h)
        # Crop the keypoint out of the image
        patch = rchip[iy1:iy2, ix1:ix2]
        subkp = kp.copy()  # subkeypoint in patch coordinates
        subkp[0:2] = (xm, ym)
        patches.append(patch)
        subkpts.append(subkp)
    return patches, subkpts


def get_warped_patches(rchip, kpts):
    'Returns warped patch around a keypoint'
    # TODO: CLEAN ME
    warped_patches = []
    warped_subkpts = []
    xs, ys = ktool.get_xys(kpts)
    # rotate relative to the gravity vector
    oris = ktool.get_oris(kpts)
    invV_mats = ktool.get_invV_mats(kpts, with_trans=False, ashomog=True)
    V_mats = ktool.get_V_mats(invV_mats)
    kpts_iter = izip(xs, ys, V_mats, oris)
    s = 41  # sf
    for x, y, V, ori in kpts_iter:
        ss = sqrt(s) * 3
        (h, w) = rchip.shape[0:2]
        # Translate to origin(0,0) = (x,y)
        T = ltool.translation_mat(-x, -y)
        R = ltool.rotation_mat(-ori)
        S = ltool.scale_mat(ss)
        X = ltool.translation_mat(s / 2, s / 2)
        M = X.dot(S).dot(R).dot(V).dot(T)
        # Prepare to warp
        dsize = np.array(np.ceil(np.array([s, s])), dtype=int)
        # Warp
        warped_patch = gtool.warpAffine(rchip, M, dsize)
        # Build warped keypoints
        wkp = np.array((s / 2, s / 2, ss, 0., ss, 0))
        warped_patches.append(warped_patch)
        warped_subkpts.append(wkp)
    return warped_patches, warped_subkpts


def get_warped_patch(imgBGR, kp, gray=False):
    kpts = np.array([kp])
    wpatches, wkpts = get_warped_patches(imgBGR, kpts)
    wpatch = wpatches[0]
    wkp = wkpts[0]
    if gray:
        wpatch = gtool.cvt_BGR2L(wpatch)
    return wpatch, wkp


def get_orientation_histogram(gori):
    # Get wrapped histogram (because we are finding a direction)
    hist_, edges_ = np.histogram(gori.flatten(), bins=8)
    hist, edges = htool.wrap_histogram(hist_, edges_)
    centers = htool.hist_edges_to_centers(edges)
    return hist, centers


def find_kpts_direction(imgBGR, kpts):
    ori_list = []
    gravity_ori = ktool.GRAVITY_THETA
    for kp in kpts:
        patch, wkp = get_warped_patch(imgBGR, kp, gray=True)
        gradx, grady = patch_gradient(patch)
        gori = patch_ori(gradx, grady)
        hist, centers = get_orientation_histogram(gori)
        # Find submaxima
        submaxima_x, submaxima_y = htool.hist_interpolated_submaxima(hist, centers)
        submax_ori = submaxima_x[submaxima_y.argmax()]
        ori = (submax_ori)  # normalize w.r.t. gravity
        ori_list.append(ori)
    _oris = np.array(ori_list, dtype=kpts.dtype)
    _oris -= gravity_ori  % np.tau  # normalize w.r.t. gravity
    # discard old orientation if they exist
    kpts2 = np.vstack((kpts[:, 0:5].T, _oris)).T
    return kpts2
