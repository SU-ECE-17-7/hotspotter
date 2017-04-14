"""
    This program will run a query for every chip in the chip table. We will then 
    export its results to a csv file which MCL will use to cluster chips to 
    represent cats. makeMatrix will need to also use csv file
"""

import numpy as np 
import csv
maxMatches = 6 #decide how many to do 

def createMatix(hs): #maybe get rid of *args and **kwargs everywhere
        size = hs.get_num_chips()
        Matrix = np.zeros((size,size))

	for chip1 in hs.get_valid_cxs(): #iterate through all chips
                ID = hs.cx2_cid(chip1)
                res_dict = {}
                res_dict = hs.query(ID)
                results = res_dict.cx2_score #i think cx2_score
                div = max(results)
                modResults = [num/div for num in results]

                """
                insert code that will create a list that has indexes
                of top matches defined by maxMatches

                """
                temp = np.nonzero(modResults)
                matches = temp[0]


                
                for score in matches:
                        if Matrix[ID-1][score -1] == 0.0:
                                Matrix[ID-1][col-1] = temp[score]
                                Matrix[col-1][ID-1] = temp[score]
                        else:
                                Matrix[ID-1][col-1] = (temp[score] + Matrix[ID-1][col-1])/2
				Matrix[col-1][ID-1] = (temp[score] + Matrix[col-1][ID-1])/2
			
		
	return Matrix
	

	
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
	
	
