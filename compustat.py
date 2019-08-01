import datetime, csv
from sas7bdat import SAS7BDAT
import pandas as pd
from timeit import default_timer as timer
import pandasql as ps

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
CSS = CS[(CS.gvkey == 1004)]
print(CS.describe)
print(CR.describe)
CS.dtypes
CR.dtypes
dates_CR = CR['datadate'].tolist() # turn date into python list
for x, item in enumerate(dates_CR):
    dates_CR[x] = "".join(item.split("-"))

CR.astype({'mdatadate': 'int64'}).dtypes

    #file.writelines('\t'.join(i) + '\n' for i in data)
CSSmerged = pd.merge(CSS, CRN, left_on=['gvkey','datadate'], right_on = ['gvkey','mdatadate'], how='left')
#df.astype({'col1': 'int32'}).dtypes
#CR.astype({'mdatadate': 'int64'}).dtypes #change variable type
#CR.rename(columns = {'datadate':'oldate'}) #ranme a variable



sqlcode = '''
select A.cusip
from A
inner join B on A.cusip=B.ncusip
where A.fdate >= B.namedt and A.fdate <= B.nameenddt
group by A.cusip
'''

newdf = ps.sqldf(sqlcode,locals())
