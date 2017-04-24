# autoquery.py
import numpy as np
''' DEPRECATED?'''

''' Autoquerying '''
def autoquery():
    numChips = hs.get_num_chips()
    scoreMat = np.zeros((numChips, numChips))
    print("[hs] beginning autoquery")
    
    ''' Make score matrix with query results '''
    for chipNum in hs.get_valid_cxs():  # For each chip
        results = hs.query(chipNum)     # Query this chip
        results = results.cx2_score     # Toss everything except the score
        
        # Normalize scores
        maxScore = max(results)
        results = [score/maxScore for score in results]
        
        '''====================='''
        #import pdb; pdb.set_trace()
        '''====================='''
        
        # Only grab nonzero values
        matches = np.nonzero(results)[0]
        
        for i in matches:                # For each matched chip,
            if scoreMat[chipNum-1][i] == 0.0:   # If these chips haven't been matched yet,
                # Insert this score
                scoreMat[chipNum-1][i] = results[i]
                scoreMat[i][chipNum-1] = results[i]
            else: # If chips have been matched by previous query,
                # Average old and new score
                scoreMat[chipNum-1][i] = (results[i] + scoreMat[chipNum-1][i])/2
                scoreMat[i][chipNum-1] = (results[i] + scoreMat[i][chipNum-1])/2
    return scoreMat
    
    
