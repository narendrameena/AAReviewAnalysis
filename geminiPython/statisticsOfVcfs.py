#!/usr/bin/python
#author narumeena
#description getting statistics out vcf files 

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

#import local files 

import queryAllVcf as qav

#getting list of all db from sub-directories 
DBFolders="/Users/naru/Documents/BISR/AAReviewPaper/dataFromIonTorrent/"


#getting variatn statistics 
def getVarState(fileList):
    #printing all results a single graph 
    listOfNumberOfVariant = []
    for db in fileList:
        #make a connection to selite db
        conn=sqlite3.connect(db)
        #make sure which db 
        print("opened : " + db)
        #de novov variants, not in dbsnp, esp and 1kg 

        #genes 
        variantNumber = conn.execute('''select count(*)  from variants where is_lof=1 AND in_esp=1 AND in_dbsnp=1 AND in_1kg=1''').fetchall()
        numVar = list(map(itemgetter(0), variantNumber)) # first column    \
        numVar.append(db)
        #put all numbers togather 
        listOfNumberOfVariant = listOfNumberOfVariant + list([numVar]) 
        conn.close()
    return listOfNumberOfVariant



if __name__ == "__main__":
    print("statisticsOfVcfs.py is being run directly")
    filelist = qav.fileList(DBFolders)
    result = getVarState( filelist)
    print(result)
    pd.DataFrame(result ).to_csv('data/knownVarNumber.csv', index=False, header=False)
else:
    print("statisticsOfVcfs.py  is being imported into another module")