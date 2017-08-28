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
results = []
for root, dirs, files in os.walk(DBFolders):
    for _file in files:
        if fnmatch.fnmatch(_file, '*.db'):
            results.append(os.path.join(root, _file))

print(results)