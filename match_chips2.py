'''Module match_chips: 
    Runs vsone, vsmany, and bagofwords matching'''
#from numba import autojit
from __future__ import division, print_function
#========================================
# IMPORTS
#========================================
# Standard library imports
import itertools
import sys
import os
import warnings
import textwrap
# Hotspotter Frontend Imports
import draw_func2 as df2
# Hotspotter Imports
import fileio as io
import helpers
from helpers import Timer, tic, toc, printWARN
from Printable import DynStruct
import algos
import helpers
import spatial_verification2 as sv2
import load_data2
import params
# Math and Science Imports
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pyflann
import scipy as sp
import scipy.sparse as spsparse
import sklearn.preprocessing 
from itertools import izip
#print('LOAD_MODULE: match_chips2.py')
from bagofwords import *

def reload_module():
    import imp, sys
    print('[mc2] reloading '+__name__)
    imp.reload(sys.modules[__name__])
def rrr():
    reload_module()

def debug_cx2_fm_shape(cx2_fm):
    print('-------------------')
    print('Debugging cx2_fm shape')
    print('len(cx2_fm)=%r' % len(cx2_fm))
    last_repr = ''
    for cx in xrange(len(cx2_fm)):
        if type(cx2_fm[cx]) == np.ndarray:
            this_repr = repr(cx2_fm[cx].shape)+repr(type(cx2_fm[cx]))
        else:
            this_repr = repr(len(cx2_fm[cx]))+repr(type(cx2_fm[cx]))
        if last_repr != this_repr:
            last_repr = this_repr
            print(last_repr)
    print('-------------------')


def ensure_array_dtype(arr, dtype):
    if not type(arr) is np.ndarray or arr.dtype != dtype:
        arr = np.array(arr, dtype=dtype)
    return arr

def ensure_2darray_nCols(arr, nCols):
    if len(arr.shape) != 2 or arr.shape[1] != nCols:
        arr = arr.reshape(len(arr), nCols)
    return arr

def fix_fm(fm):
    fm = ensure_array_dtype(fm, FM_DTYPE)
    fm = ensure_2darray_nCols(fm, 2)
    return fm

def fix_fs(fs):
    fs = ensure_array_dtype(fs, FS_DTYPE)
    fs = fs.flatten()
    return fs

def fix_cx2_fm_shape(cx2_fm):
    for cx in xrange(len(cx2_fm)):
        cx2_fm[cx] = fix_fm(cx2_fm[cx])
    cx2_fm = np.array(cx2_fm)
    return cx2_fm

#def fix_cx2_fm_shape(cx2_fm):
    #for cx in xrange(len(cx2_fm)):
        #fm = cx2_fm[cx]
        #if type(fm) != np.ndarray() or fm.dtype != FM_DTYPE:
            #fm = np.array(fm, dtype=FM_DTYPE)
        #if len(fm.shape) != 2 or fm.shape[1] != 2:
            #fm = fm.reshape(len(fm), 2)
        #cx2_fm[cx] = fm
    #cx2_fm = np.array(cx2_fm)
    #return cx2_fm

def fix_res_types(res):
    for cx in xrange(len(res.cx2_fm_V)):
        res.cx2_fm_V[cx] = np.array(res.cx2_fm_V[cx], dtype=FM_DTYPE)
    for cx in xrange(len(res.cx2_fs_V)):
        res.cx2_fs_V[cx] = np.array(res.cx2_fs_V[cx], dtype=FS_DTYPE)

def fix_qcx2_res_types(qcx2_res):
    '''
    Changes data types of cx2_fm_V and cx2_fs_V
    '''
    total_qcx = len(qcx2_res)
    fmt_str = helpers.make_progress_fmt_str(total_qcx)
    for qcx in xrange(total_qcx):
        helpers.print_(fmt_str % (qcx))
        res = qcx2_res[qcx]
        fix_res_types(res)

#=========================
# Query Result Class
#=========================

def query_result_fpath(hs, qcx, query_uid=None):
    if query_uid is None: query_uid = params.get_query_uid()
    qres_dir  = hs.dirs.qres_dir 
    fname = 'result_%s_qcx=%d.npz' % (query_uid, qcx)
    fpath = os.path.join(qres_dir, fname)
    return fpath

def query_result_exists(hs, qcx, query_uid=None):
    fpath = query_result_fpath(hs, qcx, query_uid)
    return os.path.exists(fpath)

class QueryResult(DynStruct):
    def __init__(self, qcx, hs):
        super(QueryResult, self).__init__()
        self.qcx       = qcx
        self.query_uid = params.get_query_uid()
        # Times
        self.assign_time = -1
        self.verify_time = -1
        # Assigned features matches
        self.cx2_fm = np.array([], dtype=FM_DTYPE)
        self.cx2_fs = np.array([], dtype=FS_DTYPE)
        self.cx2_score = np.array([])
        # Spatially verified feature matches
        self.cx2_fm_V = np.array([], dtype=FM_DTYPE)
        self.cx2_fs_V = np.array([], dtype=FS_DTYPE)
        self.cx2_score_V = np.array([])

    def remove_init_assigned(self):
        self.cx2_fm = np.array([], dtype=FM_DTYPE)
        self.cx2_fs = np.array([], dtype=FS_DTYPE)
        self.cx2_score = np.array([])

    def has_cache(self, hs):
        return query_result_exists(hs, self.qcx)

    def has_init_assign(self):
        return not (len(self.cx2_fm) == 0 and len(self.cx2_fm_V) != 0)

    def get_fpath(self, hs):
        return query_result_fpath(hs, self.qcx, self.query_uid)
    
    def save(self, hs, remove_init=True):
        if remove_init: self.remove_init_assigned()
        fpath = self.get_fpath(hs)
        if params.VERBOSE_CACHE:
            print('[mc2] caching result: %r' % (fpath,))
        else:
            print('[mc2] caching result: %r' % (os.path.split(fpath)[1],))
        with open(fpath, 'wb') as file_:
            np.savez(file_, **self.__dict__.copy())
        return True

    def load(self, hs, remove_init=True):
        'Loads the result from the given database'
        fpath = os.path.normpath(self.get_fpath(hs))
        try:
            with open(fpath, 'rb') as file_:
                npz = np.load(file_)
                for _key in npz.files:
                    self.__dict__[_key] = npz[_key]
                npz.close()
            self.qcx = self.qcx.tolist()
            self.query_uid = str(self.query_uid)
            if remove_init: self.remove_init_assigned()
            return True
        except Exception as ex:
            #os.remove(fpath)
            warnmsg = ('Load Result Exception : ' + repr(ex) + 
                    '\nResult was corrupted for qcx=%d' % self.qcx)
            print(warnmsg)
            warnings.warn(warnmsg)
            raise
            #return False

    def cache_bytes(self, hs):
        fpath = self.get_fpath(hs)
        return helpers.file_bytes(fpath)

    def top5_cxs(self):
        return self.topN_cxs(5)

    def topN_cxs(self, N):
        cx2_score = self.cx2_score_V
        top_cxs = cx2_score.argsort()[::-1]
        num_top = min(N, len(top_cxs))
        topN_cxs = top_cxs[0:num_top]
        return topN_cxs

#========================================
# Work Functions
#========================================

def get_dirty_test_cxs(hs):
    test_samp = hs.test_sample_cx
    print('[mc2] checking dirty queries')
    dirty_samp = [qcx for qcx in iter(test_samp) if not query_result_exists(hs, qcx)]
    return dirty_samp

def run_matching2(hs, verbose=params.VERBOSE_MATCHING):
    print(textwrap.dedent('''
    \n=============================
    [mc2] Running Matching 2
    ============================='''))
    dirty_samp = get_dirty_test_cxs(hs)
    total_dirty = len(dirty_samp)
    print('[mc2] There are %d dirty queries' % total_dirty)
    if len(dirty_samp) == 0:
        return
    print_ = helpers.print_
    if hs.matcher is None:
        hs.load_matcher()
    assign_matches  = hs.matcher.assign_matches
    cx2_desc = hs.feats.cx2_desc
    cx2_kpts = hs.feats.cx2_kpts
    cx2_rchip_size = hs.get_cx2_rchip_size()
    for qnum, qcx in enumerate(dirty_samp):
        res = QueryResult(qcx, hs)
        build_result(hs, res, cx2_kpts, cx2_desc, cx2_rchip_size,
                     assign_matches, qnum, total_dirty, verbose)

def load_cached_matches(hs):
    print_ = helpers.print_
    test_samp = hs.test_sample_cx
    # Create result containers
    print('[mc2] hs.num_cx = %r ' % hs.num_cx)
    qcx2_res = [QueryResult(qcx, hs) for qcx in xrange(hs.num_cx)]
    #--------------------
    # Read cached queries
    #--------------------
    total_queries = len(test_samp)
    print('[mc2] Total queries: %d' % total_queries)
    dirty_test_sample_cx = []
    clean_test_sample_cx = []
    fmt_str_filter = helpers.make_progress_fmt_str(total_queries, lbl='[mc2] check cache: ')
    
    # Filter queries into dirty and clean sets
    for count, qcx in enumerate(test_samp):
        print_(fmt_str_filter % (count+1))
        if params.CACHE_QUERY and qcx2_res[qcx].has_cache(hs):
            clean_test_sample_cx.append(qcx)
        else:
            dirty_test_sample_cx.append(qcx)
    print('')
    print('[mc2] Num clean queries: %d ' % len(clean_test_sample_cx))
    print('[mc2] Num dirty queries: %d ' % len(dirty_test_sample_cx))
    # Check how much data we are going to load
    num_bytes = 0
    for qcx in iter(clean_test_sample_cx):
        num_bytes += qcx2_res[qcx].cache_bytes(hs)
    print('[mc2] Loading %dMB cached results' % (num_bytes / (2.0 ** 20)))
    # Load clean queries from the cache
    fmt_str_load = helpers.make_progress_fmt_str(len(clean_test_sample_cx),
                                                 lbl='[mc2] load cache: ')
    for count, qcx in enumerate(clean_test_sample_cx):
        print_(fmt_str_load % (count+1))
        qcx2_res[qcx].load(hs)
    print('')
    return qcx2_res, dirty_test_sample_cx

def run_matching(hs, qcx2_res=None, dirty_test_sample_cx=None, verbose=params.VERBOSE_MATCHING):
    '''Runs the full matching pipeline using the abstracted classes'''
    print(textwrap.dedent('''
    \n=============================
    [mc2] Running Matching
    ============================='''))
    # Parameters
    #reverify_query       = params.REVERIFY_QUERY
    #resave_query         = params.RESAVE_QUERY
    # Return if no dirty queries
    if qcx2_res is None:
        print('[mc2] qcx2_res was not specified... loading cache')
        qcx2_res, dirty_test_sample_cx = load_cached_matches(hs)
    else:
        print('[mc2] qcx2_res was specified... not loading cache')
    if len(dirty_test_sample_cx) == 0:
        print('[mc2] No dirty queries')
        return qcx2_res
    #--------------------
    # Execute dirty queries
    #--------------------
    assign_matches  = hs.matcher.assign_matches
    cx2_desc = hs.feats.cx2_desc
    cx2_kpts = hs.feats.cx2_kpts
    cx2_rchip_size = hs.get_cx2_rchip_size()
    total_dirty = len(dirty_test_sample_cx)
    print('[mc2] Executing %d dirty queries' % total_dirty)
    for qnum, qcx in enumerate(dirty_test_sample_cx):
        if verbose:
            print('[mc2] query(%d/%d)---------------' % (qnum+1, total_dirty))
        res = qcx2_res[qcx]
        build_result(hs, res, cx2_kpts, cx2_desc, cx2_rchip_size,
                     assign_matches, verbose)
    return qcx2_res

def __build_result_assign_step(hs, res, cx2_kpts, cx2_desc, assign_matches, verbose):
    '1) Assign matches with the chosen function (vsone) or (vsmany)'
    if verbose:
        num_qdesc = len(cx2_desc[res.qcx])
        print('[mc2] assign %d desc' % (num_qdesc))
    tt1 = helpers.Timer(verbose=False)
    assign_output = assign_matches(res.qcx, cx2_desc)
    (cx2_fm, cx2_fs, cx2_score) = assign_output
    # Record initial assignments 
    res.assign_time = tt1.toc()
    res.cx2_fm      = np.array(cx2_fm)
    res.cx2_fs      = np.array(cx2_fs)
    res.cx2_score   = cx2_score

def __build_result_verify_step(hs, res, cx2_kpts, cx2_rchip_size, verbose):
    ' 2) Spatially verify the assigned matches'
    cx2_fm    = res.cx2_fm
    cx2_fs    = res.cx2_fs
    cx2_score = res.cx2_score
    if verbose:
        num_assigned = np.array([len(fm) for fm in cx2_fm]).sum()
        print('[mc2] verify %d assigned matches' % (num_assigned))
    tt2 = helpers.Timer(verbose=False)
    sv_output = spatially_verify_matches(res.qcx, cx2_kpts, cx2_rchip_size, cx2_fm, cx2_fs, cx2_score)
    (cx2_fm_V, cx2_fs_V, cx2_score_V) = sv_output
    # Record verified assignments 
    res.verify_time = tt2.toc()
    res.cx2_fm_V    = np.array(cx2_fm_V)
    res.cx2_fs_V    = np.array(cx2_fs_V)
    res.cx2_score_V = cx2_score_V
    if verbose:
        num_verified = np.array([len(fm) for fm in cx2_fm_V]).sum()
        print('[mc2] verified %d matches' % (num_verified))

def build_result(hs, res, cx2_kpts, cx2_desc, cx2_rchip_size, assign_matches,
                 verbose=True, remove_init=True):
    'Calls the actual query calculations and builds the result class'
    __build_result_assign_step(hs, res, cx2_kpts, cx2_desc, assign_matches, verbose)
    __build_result_verify_step(hs, res, cx2_kpts, cx2_rchip_size, verbose)
    if verbose:
        print('...assigned: %.2f seconds' % (res.assign_time))
        print('...verified: %.2f seconds\n' % (res.verify_time))
    else:
        print('...query: %.2f seconds\n' % (res.verify_time + res.assign_time))
    res.save(hs, remove_init=remove_init)

def build_result_qcx(hs, qcx, use_cache=True, remove_init=True, krnn=False, save_changes=False):
    'this should be the on-the-fly / Im going to check things function'
    hs.matcher.set_knn_fn(krnn)
    res = QueryResult(qcx, hs)
    if use_cache and res.has_cache(hs):
        print('[build_result_qcx] use_cache=%r, ... Loading Result' % (use_cache,))
        res.load(hs, remove_init)
        if not remove_init and res.has_init_assign():
            print('[build_result_qcx] ... Load Succesful')
            print(res)
            return res
        else:
            print('[build_result_qcx] Loading Failed.')
    else:
        print('[build_result_qcx] use_cache=%r, ... Building Result' % (use_cache,))
    verbose = True
    #print('krnn=%r' % krnn)
    #print(hs.matcher)
    assign_matches = hs.matcher.assign_matches
    cx2_desc = hs.feats.cx2_desc
    cx2_kpts = hs.feats.cx2_kpts
    cx2_rchip_size = hs.get_cx2_rchip_size()
    __build_result_assign_step(hs, res, cx2_kpts, cx2_desc, assign_matches, verbose)
    __build_result_verify_step(hs, res, cx2_kpts, cx2_rchip_size, verbose)
    if use_cache or save_changes:
        res.save(hs, remove_init=remove_init)
    return res

#========================================
# One-vs-Many 
#========================================
class VsManyArgs(DynStruct): # TODO: rename this
    '''Contains a one-vs-many index and the 
       inverted information needed for voting'''
    def __init__(self, vsmany_flann, ax2_desc, ax2_cx, ax2_fx):
        super(VsManyArgs, self).__init__()
        self.vsmany_flann = vsmany_flann
        self.ax2_desc  = ax2_desc # not used, but needs to maintain scope
        self.ax2_cx = ax2_cx
        self.ax2_fx = ax2_fx
        self.checks = 128
        self.K      = params.__VSMANY_K__
        self.checks = params.VSMANY_FLANN_PARAMS['checks']
        self.set_knn_fn(params.__USE_KRNN__)
    def set_knn_fn(self, use_reciprocal=False):
        if use_reciprocal:
            self.knn_fn  = self.reciprocal_nearest_neighbors
        else:
            self.knn_fn  = self.nearest_neighbors
    def reciprocal_nearest_neighbors(self, query, K):
        return reciprocal_nearest_neighbors(query, self.ax2_desc,
                                            self.vsmany_flann, K, self.checks)
    def nearest_neighbors(self, query, K):
        return nearest_neighbors(query, self.vsmany_flann, K, self.checks)
    def __del__(self):
        print('[mc2] Deleting VsManyArgs')

def __aggregate_descriptors(cx2_desc, indexed_cxs):
    '''Aggregates a sample set of descriptors. 
    Returns descriptors, chipxs, and featxs indexed by ax'''
    # sample the descriptors you wish to aggregate
    sx2_cx   = indexed_cxs
    sx2_desc = cx2_desc[sx2_cx]
    sx2_numfeat = [len(k) for k in iter(cx2_desc[sx2_cx])]
    cx_numfeat_iter = izip(sx2_cx, sx2_numfeat)
    # create indexes from agg desc back to chipx and featx
    _ax2_cx = [[cx]*num_feats for (cx, num_feats) in cx_numfeat_iter]
    _ax2_fx = [range(num_feats) for num_feats in iter(sx2_numfeat)]
    ax2_cx  = np.array(list(itertools.chain.from_iterable(_ax2_cx)))
    ax2_fx  = np.array(list(itertools.chain.from_iterable(_ax2_fx)))
    ax2_desc = np.vstack(cx2_desc[sx2_cx])
    return ax2_cx, ax2_fx, ax2_desc

def aggregate_descriptors_vsmany(hs):
    '''aggregates all descriptors for vsmany search'''
    print('[mc2] Aggregating descriptors for one-vs-many')
    cx2_desc  = hs.feats.cx2_desc
    indexed_cxs = hs.indexed_sample_cx
    indexed_cxs = range(hs.num_cx) if indexed_cxs is None else indexed_cxs
    return __aggregate_descriptors(cx2_desc, indexed_cxs)

#@profile
def precompute_index_vsmany(hs):
    print(textwrap.dedent('''
    \n=============================
    [mc2] Building one-vs-many index
    ============================='''))
    # Build (or reload) one vs many flann index
    cache_dir  = hs.dirs.cache_dir
    ax2_cx, ax2_fx, ax2_desc = aggregate_descriptors_vsmany(hs)
    # Precompute flann index
    matcher_uid = params.get_matcher_uid()
    #checks = params.VSMANY_FLANN_PARAMS['checks']
    vsmany_flann_params = params.VSMANY_FLANN_PARAMS
    vsmany_flann = algos.precompute_flann(ax2_desc, 
                                          cache_dir=cache_dir,
                                          uid=matcher_uid,
                                          flann_params=vsmany_flann_params)
    # Return a one-vs-many structure
    vsmany_args = VsManyArgs(vsmany_flann, ax2_desc, ax2_cx, ax2_fx)
    return vsmany_args

# Feature scoring functions
eps = 1E-8
def LNRAT_fn(vdist, ndist): return np.log(np.divide(ndist, vdist+eps)+1) 
def RATIO_fn(vdist, ndist): return np.divide(ndist, vdist+eps)
def LNBNN_fn(vdist, ndist): return (ndist - vdist) / 1000.0

scoring_func_map = {
    'LNRAT' : LNRAT_fn,
    'RATIO' : RATIO_fn,
    'LNBNN' : LNBNN_fn }

def desc_nearest_neighbors(desc, vsmany_args, K=None):
    vsmany_flann = vsmany_args.vsmany_flann
    ax2_cx       = vsmany_args.ax2_cx
    ax2_fx       = vsmany_args.ax2_fx
    isQueryIndexed = True
    K = params.__VSMANY_K__ if K is None else K
    checks   = params.VSMANY_FLANN_PARAMS['checks']
    # Find each query descriptor's k+1 nearest neighbors
    (qfx2_ax, qfx2_dists) = vsmany_flann.nn_index(desc, K, checks=checks)
    qfx2_cx = ax2_cx[qfx2_ax]
    qfx2_fx = ax2_fx[qfx2_ax]
    return (qfx2_cx, qfx2_fx, qfx2_dists) 

# TODO: Nearest Neighbor Huristrics 
# K-recripricol nearest neighbors
# ROI spatial matching
# Frequency Reranking


def nearest_neighbors(qfx2_desc, data_flann, K, checks):
    'Plain Nearest Neighbors'
    (qfx2_dx, qfx2_dists) = data_flann.nn_index(qfx2_desc, K, checks=checks)
    # All neighbors are valid
    qfx2_valid = np.ones(qfx2_dx.shape, dtype=np.bool)
    return qfx2_dx, qfx2_dists, qfx2_valid

# TODO: For Spatial Nearest Neighbors
# 1) Change kpts to be in the range 0 to 1
# 2) Make a quick lookup table for chip size
'''
K = 3
qfx2_xy1 = np.array([(.1, .1), (.2, .2), (.3, .3)])
qfx2_xy2 = np.array([((.1, .1), (.2, .2), (.3, .3)), 
                     ((.1, .1), (.2, .2), (.3, .3)), 
                     ((.1, .1), (.2, .2), (.3, .3)), 
                     ((.1, .1), (.2, .2), (.3, .3)) ])
arr = qfx2_xy2
'''

def tile_before_axis(arr, axis, num):
    repl = tuple([num] + ([1]*len(arr.shape)))
    rollax = np.rollaxis
    tile  = np.tile
    return rollax(rollax(tile(rollax(arr, axis, 0), repl), 0, axis+2), 0, axis+2)
    #roll1 = np.rollaxis(arr, axis, 0)
    #tarr = np.tile(roll1, repl)
    #tarr2 = np.rollaxis(tarr, 0, axis+2)
    #tarr3 = np.rollaxis(tarr2, 0, axis+2)
    #print(arr.shape)
    #print(roll1.shape)
    #print(tarr.shape)
    #print(tarr2.shape)
    #print(tarr3.shape)

def snn_testdata(hs):
    hs.ensure_matcher_type('vsmany')
    vsmany_args = hs.matcher.vsmany_args
    cx2_desc = hs.feats.cx2_desc
    cx2_kpts = hs.feats.cx2_kpts
    qcx = 0
    qfx2_desc = cx2_desc[qcx]
    qfx2_kpts = cx2_kpts[qcx]
    cx2_rchip_size = hs.get_cx2_rchip_size()
    qchipdiag = np.sqrt((np.array(cx2_rchip_size[qcx])**2).sum())
    data_flann = vsmany_args.vsmany_flann
    dx2_desc = vsmany_args.ax2_desc
    dx2_cx = vsmany_args.ax2_cx
    dx2_fx = vsmany_args.ax2_fx
    K = 3
    checks = 128

def spatial_nearest_neighbors(qfx2_desc, qfx2_kpts, qchipdiag, dx2_desc, dx2_kpts, dx2_cx, data_flann, K, checks):
    'K Spatial Nearest Neighbors'
    nQuery, dim = qfx2_desc.shape
    # Get nearest neighbors #.2690s 
    (qfx2_dx, qfx2_dists) = data_flann.nn_index(qfx2_desc, K, checks=checks)
    # Get matched chip sizes #.0300s
    qfx2_cx = dx2_cx[qfx2_dx]
    qfx2_fx = dx2_fx[qfx2_dx]
    qfx2_chipsize2 = np.array([cx2_rchip_size[cx] for cx in qfx2_cx.flat])
    qfx2_chipsize2.shape = (nQuery, K, 2)
    qfx2_chipdiag2 = np.sqrt((qfx2_chipsize2**2).sum(2))
    # Get query relative xy keypoints #.0160s / #.0180s (+cast)
    qfx2_xy1 = np.array(qfx2_kpts[:, 0:2], np.float)
    qfx2_xy1[:,0] /= qchipdiag
    qfx2_xy1[:,1] /= qchipdiag
    # Get database relative xy keypoints
    qfx2_xy2 = np.array([cx2_kpts[cx][fx, 0:2] for (cx, fx) in
                         izip(qfx2_cx.flat, qfx2_fx.flat)], np.float)
    qfx2_xy2.shape = (nQuery, K, 2)
    qfx2_xy2[:,:,0] /= qfx2_chipdiag2
    qfx2_xy2[:,:,1] /= qfx2_chipdiag2
    # Get the relative distance # .0010s
    qfx2_K_xy1 = np.rollaxis(np.tile(qfx2_xy1, (K, 1, 1)), 1)
    qfx2_xydist = ((qfx2_K_xy1 - qfx2_xy2)**2).sum(2)
    qfx2_dist_valid = qfx2_xydist < .5

    # Do scale for funzies
    qfx2_det1 = np.array(qfx2_kpts[:, [2,4]], np.float).prod(1)
    qfx2_det1 = np.sqrt(1.0/qfx2_det1)
    qfx2_K_det1 = np.rollaxis(np.tile(qfx2_det1, (K, 1)), 1)
    qfx2_det2 = np.array([cx2_kpts[cx][fx, [2,4]] for (cx, fx) in
                          izip(qfx2_cx.flat, qfx2_fx.flat)], np.float).prod(1)
    qfx2_det2.shape = (nQuery, K)
    qfx2_det2 = np.sqrt(1.0/qfx2_det2)
    qfx2_scaledist = qfx2_det2 / qfx2_K_det1

    qfx2_scale_valid = np.bitwise_and(qfx2_scaledist > .5, qfx2_scaledist < 2)
    
    # All neighbors are valid
    qfx2_valid = np.bitwise_and(qfx2_dist_valid, qfx2_scale_valid)
    return qfx2_dx, qfx2_dists, qfx2_valid

def reciprocal_nearest_neighbors(qfx2_desc, dx2_desc, data_flann, K, checks):
    'K Reciprocal Nearest Neighbors'
    nQuery, dim = qfx2_desc.shape
    # Assign query features to K nearest database features
    (qfx2_dx, qfx2_dists) = data_flann.nn_index(qfx2_desc, K, checks=checks)
    # Assign those nearest neighbors to K nearest database features
    qx2_nn = dx2_desc[qfx2_dx]
    qx2_nn.shape = (nQuery*K, dim)
    (_nn2_dx, nn2_dists) = data_flann.nn_index(qx2_nn, K, checks=checks)
    # Get the maximum distance of the reciprocal neighbors
    nn2_dists.shape = (nQuery, K, K)
    qfx2_maxdist = nn2_dists.max(2)
    # Test if nearest neighbor distance is less than reciprocal distance
    qfx2_valid = qfx2_dists < qfx2_maxdist
    return qfx2_dx, qfx2_dists, qfx2_valid 


#@profile
def assign_matches_vsmany(qcx, cx2_desc, vsmany_args):
    '''Matches qdesc vs all database descriptors using 
    Input:
        qcx        - query chip index
        cx2_desc    - chip descriptor lookup table
        vsmany_args - class with FLANN index of database descriptors
    Output: 
        cx2_fm - C x Mx2 array of matching feature indexes
        cx2_fs - C x Mx1 array of matching feature scores'''

    # vsmany_args = hs.matcher.vsmany_args
    #helpers.println('Assigning vsmany feature matches from qcx=%d to %d chips'\ % (qcx, len(cx2_desc)))
    isQueryIndexed = True
    k_vsmany     = vsmany_args.K + isQueryIndexed
    checks       = vsmany_args.checks
    vsmany_flann = vsmany_args.vsmany_flann
    ax2_cx       = vsmany_args.ax2_cx
    ax2_fx       = vsmany_args.ax2_fx
    ax2_desc     = vsmany_args.ax2_desc
    score_fn = scoring_func_map[params.__VSMANY_SCORE_FN__]
    qdesc = cx2_desc[qcx]
    # Find each query descriptor's k+1 nearest neighbors
    (qfx2_ax, qfx2_dists, qfx2_valid) = vsmany_args.knn_fn(qdesc, k_vsmany+1)
    qfx2_valid = qfx2_valid[:, 0:k_vsmany]
    vote_dists = qfx2_dists[:, 0:k_vsmany]
    norm_dists = qfx2_dists[:, k_vsmany] # k+1th descriptor for normalization
    # Score the feature matches
    qfx2_score = np.array([score_fn(_vdist.T, norm_dists)
                           for _vdist in vote_dists.T]).T
    # Vote using the inverted file 
    qfx2_cx = ax2_cx[qfx2_ax[:, 0:k_vsmany]]
    qfx2_fx = ax2_fx[qfx2_ax[:, 0:k_vsmany]]
    # Build feature matches
    cx2_fm = [[] for _ in xrange(len(cx2_desc))]
    cx2_fs = [[] for _ in xrange(len(cx2_desc))]
    nQuery = len(qdesc)
    qfx2_qfx = helpers.tiled_range(nQuery, k_vsmany)
    #iter_matches = izip(qfx2_qfx.flat, qfx2_cx.flat, qfx2_fx.flat, qfx2_score.flat)
    iter_matches = izip(qfx2_qfx[qfx2_valid],
                        qfx2_cx[qfx2_valid],
                        qfx2_fx[qfx2_valid],
                        qfx2_score[qfx2_valid])
    for qfx, cx, fx, score in iter_matches:
        if qcx == cx: 
            continue # dont vote for yourself
        cx2_fm[cx].append((qfx, fx))
        cx2_fs[cx].append(score)
    # Convert to numpy
    for cx in xrange(len(cx2_desc)):
        fm = np.array(cx2_fm[cx], dtype=FM_DTYPE)
        fm = fm.reshape(len(fm), 2)
        cx2_fm[cx] = fm
    for cx in xrange(len(cx2_desc)): 
        cx2_fs[cx] = np.array(cx2_fs[cx], dtype=FS_DTYPE)
    cx2_fm = np.array(cx2_fm)
    cx2_fs = np.array(cx2_fs)
    cx2_score = np.array([np.sum(fs) for fs in cx2_fs])
    return cx2_fm, cx2_fs, cx2_score

def assign_matches_vsmany_BINARY(qcx, cx2_desc):
    return None

#========================================
# One-vs-One 
#========================================
class VsOneArgs(DynStruct):
    ''' Thresholds: 
        ratio_thresh = 1.2 - keep if dist(2)/dist(1) > ratio_thresh
        burst_thresh = 1   - keep if 0 < matching_freq(desc1) <= burst_thresh '''
    def __init__(self, **kwargs):
        self.cxs          = None
        self.knn_fn       = None
        self.burst_thresh = None
        self.ratio_thresh = params.__VSONE_RATIO_THRESH__
        self.flann_params = params.VSONE_FLANN_PARAMS
        self.checks       = self.flann_params['checks']
        self.__dict__.update(kwargs)

def assign_matches_vsone(qcx, cx2_desc, vsone_args):
    ''' assigns matches from qcx to all cxs unless cxs is specifid'''
    #print('[mc2] Assigning vsone feature matches from cx=%d to %d chips'\ % (qcx, len(cx2_desc)))
    if vsone_args is None:
        vsone_args = VsOneArgs()
    cxs = xrange(len(cx2_desc)) if vsone_args.cxs is None else vsone_args.cxs
    desc1 = cx2_desc[qcx]
    vsone_flann = pyflann.FLANN()
    vsone_flann.build_index(desc1, **vsone_args.flann_params)
    cx2_fm = [[] for _ in xrange(len(cx2_desc))]
    cx2_fs = [[] for _ in xrange(len(cx2_desc))]
    sys.stdout.write('assign_matches_vsone')
    for cx in iter(cxs):
        desc2 = cx2_desc[cx]
        sys.stdout.write('.')
        #sys.stdout.flush()
        if cx == qcx: continue
        (fm, fs) = match_vsone(desc2, vsone_flann, vsone_args)
        cx2_fm[cx] = fm
        cx2_fs[cx] = fs
    sys.stdout.write('DONE')
    vsone_flann.delete_index()
    cx2_fm = np.array(cx2_fm)
    cx2_fs = np.array(cx2_fs)
    cx2_score = np.array([np.sum(fs) for fs in cx2_fs])
    return cx2_fm, cx2_fs, cx2_score

#@profile
def match_vsone(desc2, vsone_flann, vsone_args):
    '''Matches desc2 vs desc1 using Lowe's ratio test
    Input:
        desc2         - other descriptors (N2xD)
        vsone_flann   - FLANN index of desc1 (query descriptors (N1xD)) 
    Output: 
        fm - Mx2 array of matching feature indexes
        fs - Mx1 array of matching feature scores '''
    # features to their matching query features
    checks = vsone_args.checks
    (fx2_qfx, fx2_dist) = vsone_flann.nn_index(desc2, 2, checks=checks)
    # RATIO TEST
    fx2_ratio  = np.divide(fx2_dist[:, 1], fx2_dist[:, 0]+1E-8)
    fx_passratio, = np.where(fx2_ratio > vsone_args.ratio_thresh)
    fx = fx_passratio
    # BURSTINESS TEST
    if not vsone_args.burst_thresh is None:
        fx = filter_bursty_matches(fx2_qfx, fx, vsone_args.burst_thresh)
    # RETURN vsone matches and scores
    qfx = fx2_qfx[fx, 0]
    fm  = np.array(zip(qfx, fx), dtype=FM_DTYPE)
    #fm  = fm.reshape(len(fm), 2)
    fm.shape = (len(fm), 2)
    fs  = np.array(fx2_ratio[fx], dtype=FS_DTYPE)
    return (fm, fs)

def filter_bursty_matches(fx2_qfx, fx, burst_thresh):
    ''' Find frequency of descriptor matches. Convert qfx to fx
    Select the query features which only matched < burst_thresh'''
    qfx2_frequency = np.bincount(fx2_qfx[:, 0])
    qfx_nonzero    = qfx2_frequency > 0
    qfx_nonbursty  = qfx2_frequency <= burst_thresh
    qfx_nonbursty_unique, = np.where(
        np.bitwise_and(qfx_nonzero, qfx_nonbursty))
    _qfx_set      = set(qfx_nonbursty_unique.tolist())
    fx2_nonbursty = [_qfx in _qfx_set for _qfx in iter(fx2_qfx[:, 0])]
    fx_nonbursty, = np.where(fx2_nonbursty)
    fx  = np.intersect1d(fx, fx_nonbursty, assume_unique=True)
    return fx

def cv2_match(desc1, desc2):
    K = 1
    cv2_matcher = cv2.DescriptorMatcher_create('BruteForce-Hamming')
    raw_matches = cv2_matcher.knnMatch(desc1, desc2, K)
    matches = [(m1.trainIdx, m1.queryIdx) for m1 in raw_matches]

#========================================
# Spatial verifiaction 
#========================================
def __default_sv_return():
    'default values returned by bad spatial verification'
    #H = np.eye(3)
    fm_V = np.empty((0, 2))
    fs_V = np.array((0, 1))
    return (fm_V, fs_V)
#@profile
def spatially_verify(kpts1, kpts2, rchip_size2, fm, fs):
    '''1) compute a robust transform from img2 -> img1
       2) keep feature matches which are inliers 
       returns fm_V, fs_V, H '''
    # Return if pathological
    min_num_inliers   = 4
    if len(fm) < min_num_inliers:
        return __default_sv_return()
    # Get homography parameters
    xy_thresh         = params.__XY_THRESH__
    scale_thresh_high = params.__SCALE_THRESH_HIGH__
    scale_thresh_low  = params.__SCALE_THRESH_LOW__
    if params.__USE_CHIP_EXTENT__:
        diaglen_sqrd = rchip_size2[0]**2 + rchip_size2[1]**2
    else:
        x_m = kpts2[fm[:,1],0].T
        y_m = kpts2[fm[:,1],1].T
        diaglen_sqrd = sv2.calc_diaglen_sqrd(x_m, y_m)
    # Try and find a homography
    sv_tup = sv2.homography_inliers(kpts1, kpts2, fm,
                                    xy_thresh, 
                                    scale_thresh_high,
                                    scale_thresh_low,
                                    diaglen_sqrd,
                                    min_num_inliers)
    if sv_tup is None:
        return __default_sv_return()
    # Return the inliers to the homography
    (H, inliers, Aff, aff_inliers) = sv_tup
    fm_V = fm[inliers, :]
    fs_V = fs[inliers, :]
    return fm_V, fs_V

def spatially_verify_check_args(xy_thresh=None,
                                scale_min=None,
                                scale_max=None,
                                rchip_size2=None, 
                                min_num_inliers=None):
    ''' Performs argument checks for spatially_verify'''
    if min_num_inliers is None: 
        min_num_inliers = 4
    if xy_thresh is None:
        xy_thresh = params.__XY_THRESH__
    if scale_min is None:
        scale_min = params.__SCALE_THRESH_LOW__
    if scale_max is None:
        scale_max = params.__SCALE_THRESH_HIGH__
    if rchip_size2 is None:
        x_m = kpts2[fm[:,1],0].T
        y_m = kpts2[fm[:,1],1].T
        x_extent_sqrd = (x_m.max() - x_m.min()) ** 2
        y_extent_sqrd = (y_m.max() - y_m.min()) ** 2
        diaglen_sqrd = x_extent_sqrd + y_extent_sqrd
    else:
        diaglen_sqrd = rchip_size2[0]**2 + rchip_size2[1]**2
    return min_num_inliers, xy_thresh, scale_max, scale_min, diaglen_sqrd

def __spatially_verify(kpts1, kpts2, fm, fs, min_num_inliers, xy_thresh,
                       scale_thresh_high, scale_thresh_low, diaglen_sqrd):
    '''Work function for spatial verification'''
    sv_tup = sv2.homography_inliers(kpts1, kpts2, fm,
                                    xy_thresh, 
                                    scale_thresh_high,
                                    scale_thresh_low,
                                    diaglen_sqrd,
                                    min_num_inliers)
    if not sv_tup is None:
        # Return the inliers to the homography
        (H, inliers, Aff, aff_inliers) = sv_tup
        fm_V = fm[inliers, :]
        fs_V = fs[inliers, :]
    else:
        fm_V = np.empty((0, 2))
        fs_V = np.array((0, 1))
        H = np.eye(3)
    return fm_V, fs_V, H


def spatially_verify2(kpts1, kpts2, fm, fs, **kwargs):
    '''Wrapper function for spatial verification with argument checks'''
    min_num_inliers, xy_thresh, scale_min, scale_max, diaglen_sqrd = spatially_verify_check_args(**kwargs)
    fm_V, fs_V, H = __spatially_verify(kpts1, kpts2, fm, fs, min_num_inliers,
                                       xy_thresh, scale_min, scale_max, diaglen_sqrd)
    return fm_V, fs_V


#@profile
def spatially_verify_matches(qcx, cx2_kpts, cx2_rchip_size, cx2_fm, cx2_fs, cx2_score):
    kpts1     = cx2_kpts[qcx]
    #cx2_score = np.array([np.sum(fs) for fs in cx2_fs])
    top_cx     = cx2_score.argsort()[::-1]
    num_rerank = min(len(top_cx), params.__NUM_RERANK__)
    # Precompute output container
    cx2_fm_V = [[] for _ in xrange(len(cx2_fm))]
    cx2_fs_V = [[] for _ in xrange(len(cx2_fs))]
    # spatially verify the top __NUM_RERANK__ results
    for topx in xrange(num_rerank):
        cx    = top_cx[topx]
        kpts2 = cx2_kpts[cx]
        fm    = cx2_fm[cx]
        fs    = cx2_fs[cx]
        rchip_size2 = cx2_rchip_size[cx]
        fm_V, fs_V = spatially_verify(kpts1, kpts2, rchip_size2, fm, fs)
        cx2_fm_V[cx] = fm_V
        cx2_fs_V[cx] = fs_V
    # Rebuild the feature match / score arrays to be consistent
    for cx in xrange(len(cx2_fm_V)):
        fm = np.array(cx2_fm_V[cx], dtype=FM_DTYPE)
        fm = fm.reshape(len(fm), 2)
        cx2_fm_V[cx] = fm
    for cx in xrange(len(cx2_fs_V)): 
        cx2_fs_V[cx] = np.array(cx2_fs_V[cx], dtype=FS_DTYPE)
    cx2_fm_V = np.array(cx2_fm_V)
    cx2_fs_V = np.array(cx2_fs_V)
    # Rebuild the cx2_score arrays
    cx2_score_V = np.array([np.sum(fs) for fs in cx2_fs_V])
    return cx2_fm_V, cx2_fs_V, cx2_score_V

#=========================
# Matcher Class
#=========================
class Matcher(DynStruct):
    '''Wrapper class: assigns matches based on
       matching and feature prefs'''
    def __init__(self, hs, match_type=None):
        super(Matcher, self).__init__()
        print('[mc2] Creating matcher: '+str(match_type))
        self.match_type = match_type
        # Possible indexing structures
        self.vsmany_args = None
        self.vsone_args  = None
        self.bow_args    = None
        # Curry the correct functions
        self.__assign_matches = None
        if not match_type is None: 
            self.set_match_type(hs, match_type)

    def ensure_match_type(self, hs, match_type):
        if self.match_type != match_type:
            return self.set_match_type(hs, match_type)

    def set_match_type(self, hs, match_type):
        self.match_type = match_type
        if match_type == 'bagofwords':
            print('[mc2] precomputing bag of words')
            self.bow_args   = precompute_bag_of_words(hs)
            self.__assign_matches = self.__assign_matches_bagofwords
        elif match_type == 'vsmany':
            print('[mc2] precomputing one vs many')
            self.vsmany_args = precompute_index_vsmany(hs)
            self.__assign_matches = self.__assign_matches_vsmany
        elif match_type == 'vsone':
            self.vsone_args = VsOneArgs()
            self.__assign_matches = self.__assign_matches_vsone
        else:
            raise Exception('Unknown match_type: '+repr(match_type))

    def assign_matches(self, qcx, cx2_desc):
        'Function which calls the correct matcher'
        return self.__assign_matches(qcx, cx2_desc)
    def set_knn_fn(self, use_reciprocal):
        print('[matcher] set_knn_fn  %r ' % use_reciprocal)
        params.__USE_KRNN__ = use_reciprocal
        if not self.vsmany_args is None:
            self.vsmany_args.set_knn_fn(use_reciprocal)
    # query helpers
    def __assign_matches_vsone(self, qcx, cx2_desc):
        return assign_matches_vsone(qcx, cx2_desc, self.vsone_args)
    def __assign_matches_vsmany(self, qcx, cx2_desc):
        return assign_matches_vsmany(qcx, cx2_desc, self.vsmany_args)
    def __assign_matches_bagofwords(self, qcx, cx2_desc):
        return assign_matches_bagofwords(qcx, cx2_desc, self.bow_args)
    def __del__(self):
        print('[mc2] Deleting Matcher')


def matcher_test(hs, qcx, fnum=1):
    hs.ensure_matcher_type('vsmany')
    use_cache = True
    res  = build_result_qcx(hs, qcx, use_cache=use_cache, remove_init=False, krnn=False, save_changes=True )
    res2 = build_result_qcx(hs, qcx, use_cache=use_cache, remove_init=False, krnn=True, save_changes=True)
    N = 5
    df2.show_match_analysis(hs, res, N, fnum); fnum += 1
    df2.show_match_analysis(hs, res2, N, fnum); fnum += 1
    #for cx in hs.get_other_indexed_cxs(qcx):
        #df2.figure(fignum=fnum)
        #df2.show_matches_annote_res(res, hs, cx, draw_pts=False, plotnum=(2,2,1), SV=False)
        #df2.show_matches_annote_res(res, hs, cx, draw_pts=False, plotnum=(2,2,2), SV=True)
        #df2.show_matches_annote_res(res2, hs, cx, draw_pts=False, plotnum=(2,2,3), SV=False)
        #df2.show_matches_annote_res(res2, hs, cx, draw_pts=False, plotnum=(2,2,4), SV=True)
        #fnum += 1
    return fnum

if __name__ == '__main__':
    from multiprocessing import freeze_support
    import load_data2
    import chip_compute2
    import params
    freeze_support()
    print('[mc2] __main__ = match_chips2.py')

    # --- CHOOSE DATABASE --- #
    db_dir = params.DEFAULT
    hs = load_data2.HotSpotter()
    hs.load_tables(db_dir)
    hs.load_chips()
    hs.set_samples()
    hs.load_features()
    hs.load_matcher()

    #qcx = 111
    #cx = 305
    qcx = helpers.get_arg_after('--qcx', type_=int)
    if qcx is None: qcx = 0
    matcher_test(hs, qcx)

    exec(df2.present())
