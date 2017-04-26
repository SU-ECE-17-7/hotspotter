"""
    This program will run a query for every chip in the chip table. We will then 
    export its results to a csv file which MCL will use to cluster chips to 
    represent cats. makeMatrix will need to also use csv file
"""

import numpy as np 
import csv

SAME_IMAGE_WEIGHT = .9
SAME_SET_WEIGHT =  1

def createMatrix(hs): #maybe get rid of *args and **kwargs everywhere
        size = hs.get_num_chips()
        Matrix = np.zeros((size,size))
        
	for i in hs.get_valid_cxs(): #iterate through all chips
                chip1 = hs.cx2_cid(i)
		chip1Name = hs.cx2_gname(i)
	        res_dict = {}
                res_dict = hs.query(chip1)
                results = res_dict.cx2_score 
                div = max(results)
                if div > 0.0:
                        results = [num/div for num in results]
 		for j in hs.get_valid_cxs():
			chip2 = hs.cx2_cid(j)
			chip2Name = hs.cx2_gname(j)
			if chip1!=chip2:
				if sameImage(chip1Name, chip2Name):
					Matrix[i][j] = SAME_IMAGE_WEIGHT
					Matrix[j][i] = SAME_IMAGE_WEIGHT
			        elif sameSet(chip1Name, chip2Name) and Matrix[i][j] == 0.0:
                                        Matrix[i][j] = (results[j] + SAME_SET_WEIGHT)/2
				        Matrix[j][i] = (results[j] + SAME_SET_WEIGHT)/2
				elif sameSet(chip1Name, chip2Name) and Matrix[i][j] != 0.0:
					Matrix[i][j] = (((Matrix[i][j] + results[j])/2) + SAME_SET_WEIGHT)/2
					Matrix[j][i] = (((Matrix[j][i] + results[j])/2) + SAME_SET_WEIGHT)/2
				elif not sameSet(chip1Name, chip2Name) and Matrix[i][j] == 0.0:
					Matrix[i][j] = results[j] 
					Matrix[j][i] = results[j]
				else:
					Matrix[i][j] = (Matrix[i][j] + results[j])/2
					Matrix[j][j] = (Matrix[j][i] + results[j])/2
                                        
	return Matrix
	





def sameSet(chip1, chip2):
        
        #if in same location
        if getLoc(chip1) == getLoc(chip2):
                #if on same date
                if getDate(chip1) == getDate(chip2):
                        #print "same location and date"
                        
                        #if close time
                        if np.abs(getTime(chip1) - getTime(chip2)) <= secsThresh:
                                #print "within secsThresh"
                                return True
                        else:
                                #print "not within secsThresh"
                                return False
                        #elif one day apart but still less than 90 second:
                        #    (getTime(chip1) <= secsThresh or
                        #     getTime(chip1) > (secsInDay - secThresh)):
                        #check dates still
                        
                else:
                        #print "not same date"
                        return False
        else:
                #print "not same location"
                return False


def getLoc(chip):
        chipList = chip.split("__")
        loc = (chipList[0] + "__" + chipList[1] +"__"+chipList[2])
        return loc

def getDate(chip):
        date  = chip.split("__")[3]
        return date

#def getDateInDays(date):
# figure out if stuff happened at end of a month (or year...)

def getTime(chip):
        chipList = chip.split("__")
        timeStr = chipList[4]
        
        timeStr = timeStr.split("(")[0]
        timeList = timeStr.split("-")
        
        time = int(timeList[0])*3600 + int(timeList[1])*60 + int(timeList[2])

        return time

	
def sameImage(chip1, chip2):
        
	if chip1 == chip2:
		return True
	else:
		return False
        
	
def createFile(hs, Mat):
        size = hs.get_num_chips()
	file_obj = open("Matrix.csv", "w")
	for row in range(size):
		for col in range(size-1): 
			file_obj.write(str(Mat[row,col]) + ",")
		file_obj.write(str(Mat[row,size-1]) +"\n")
        #print "file created"

	
if __name__ == "__main__":
	Matrix = createMatrix(hs)
	createFile(hs, Matrix)
	
	
