import datetime, csv
from sas7bdat import SAS7BDAT
import pandas as pd
from timeit import default_timer as timer

count = 0
COMP_CR = 'C:/Users/Panqiao/Documents/Research/SS - All/COMPSTAT/adsprate.sas7bdat'
COMP_CRS = 'C:/Users/Panqiao/Documents/Research/SS - All/COMPSTAT/cpstCR.txt'
COMP_COMP = 'C:/Users/Panqiao/Documents/Research/SS - All/COMPSTAT/COMPSTAT_all_vars_1970_20150301.txt'
#COMP_CR = 'C:/Users/Panqiao/Documents/Research/SS - All/COMPSTAT/names_adsprate.sas7bdat'
#with SAS7BDAT(COMP_CR, skip_header=False) as reader:
   # print(reader[0])

    #for row in reader:
        #print(row)
        #count += 1
        #if count == 1000:
            #break
        #break


def sas_to_dataframe(file_path):
    """
    Read in a SAS dataset (sas7bdat) with the proper encoding
    :param file_path: location of SAS dataset to be read in
    :return: pandas dataframe with contents of SAS dataset
    """
    return pd.read_sas(COMP_CR, format="sas7bdat", encoding="iso-8859-1")


#CR = sas_to_dataframe(COMP_CR)
#CR.to_csv(COMP_CRS)

CS = pd.read_csv(COMP_COMP, sep="\t", nrows=1000, usecols=[0, 1,2 ,3 ,925 ,1823] )#, header=None)
CR = pd.read_csv(COMP_CRS, sep=",", nrows=1000)
print(CS.describe)
print(CR.describe)
CS.dtypes
CR.dtypes
#print(CR.describe)
#print(CR['gvkey'])
#fhand_COMP = [x[0] for x in csv.reader(open(COMP_COMP,'r') , delimiter='\t')]
#line = open(COMP_COMP).readline().split()
#print(line)
#print(type(line))
#line = open(COMP_COMP).readline().split()
#lines = open(COMP_COMP).readlines()
#crispy = line [0:10]
#for i, item in enumerate(line):
    #if item == 'at':
        #print(i, item)
    #if 'sic' in item:
        #print(i, item)
#at 94
#gvkey 0
#datadate 1
#fyear 2
#indfmt 3
#sich 925
#sic 1823
#count = 0
#while count < 11:
#print(len(lines))
#for i in range(0:len(lines))
    #crispy = lines[count:count+1]
    #line_1 = [line.split("\t") for line in crispy]
    #print(line_1)
    #count += 1
