#!/usr/bin/python
#author narumeena
#making matrix out or all vcf files for diffrent typr of variants 

import subprocess
import sqlite3
import numpy as np
import pandas as pd
from scipy import stats, integrate
import matplotlib.pyplot as plt
import seaborn as sns
from operator import itemgetter #
import csv
import os
import re
import fnmatch

#getting list of all db from sub-directories 
DBFolders="/Users/naru/Documents/BISR/AAReviewPaper/dataFromIonTorrent/"


##getting all db files 

def fileList(DBFolders):
    results = []
    #making a array list of all db files found in folder 
    for root, dirs, files in os.walk(DBFolders):
        for _file in files:
            if fnmatch.fnmatch(_file, '*.db'):
                results.append(os.path.join(root, _file))
    return results
#print(results)
#print(len(results))



#getting all varaints location 

def getVarLocation(results):
    #printing all results a single graph 
    allVariants = []
    for db in results:
        #make a connection to selite db
        conn=sqlite3.connect(db)
        #make sure which db 
        print("opened : " + db)
        #de novov variants, not in dbsnp, esp and 1kg 
        variantNotInDB = conn.execute('''select chrom, start, end   from variants where is_lof=1 AND in_esp=1 AND in_dbsnp=1 AND in_1kg=1''').fetchall()
        chrom = list(map(itemgetter(0), variantNotInDB)) # first column 
        
        #print("chrom : " + str(len(chrom)) +  "\n")
        chrom = [x.encode("utf-8") for x in chrom]
        #print(chrom)
        start= list(map(itemgetter(1), variantNotInDB)) # second column 
        #print("start : " + str(len(start)) +  "\n")
        #print(start)
        end= list(map(itemgetter(2), variantNotInDB)) # third column 
        #print("start : " + str(len(end)) +  "\n")
        variantLocation = zip(chrom, start, end)
        #print(end)
        
        #put all variants togather 
        allVariants = allVariants + list(set(list(variantLocation)) - set(allVariants))

        #making csv on the basis of matches 
        #LookupByTuple(tupl= variantLocation,matrx= [list(row) for row in allVariants])
        
        conn.close()
    return allVariants


####looping over each variant and get info related to it.  
def makingDataFrame(allVariants, results):
    variantDf = pd.DataFrame(index=allVariants, columns=results)  # panda empty dataframe 

    variantDf = variantDf.fillna(0) #fill it with zeroes 
    #print(variantDf.iloc[1])
    output = pd.DataFrame(index=allVariants, columns=results)
    for index, row in variantDf.iterrows():
        #print(index[0])
        for db in results:
                #make a connection to selite db
            conn=sqlite3.connect(db)
            #make sure which db 
            #print("opened : " + db)
            #de novov variants, not in dbsnp, esp and 1kg 
            #print(db)
            #print(db.split("/"))
            #print(db.split("/")[7])
            variant = conn.execute('''select gene from variants WHERE is_lof=1 AND chrom like "%'''+index[0] +'''%" AND start =''' +str(index[1])+''' AND end = ''' +str(index[2])).fetchall()
            encodeVar = list(map(itemgetter(0), variant))
            encodeVar = [x.encode("utf-8") for x in encodeVar] #uncomment if output is character 
            if len(encodeVar)== 0: # cheking if list is empty or not 
                encodeVar=""
            else:
                encodeVar =encodeVar[0]
            output.set_value(index,db,encodeVar)
            #print(list(map(itemgetter(1), variantNotInDB)))
            conn.close()
    return output    
    


 # with 0s rather than NaNs
#print([list(row) for row in allVariants])


if __name__ == "__main__":
    print("queryAllVcf.py is being run directly")
    results = fileList(DBFolders)
    allVariants = getVarLocation(results)   
    #print(output)
    print([i.split("/")[7] for i in results])
    outputFileName= "data/output.csv"
    csvOut = makingDataFrame(allVariants, results  )
    csvOut.columns = [i.split("/")[7] for i in results]
    csvOut.to_csv(outputFileName , sep=',')
    print("successful")
else:
    print("queryAllVcf.py is being imported into another module")


