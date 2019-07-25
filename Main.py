import os, csv, compfuncs
#Match data to CRSP PEMRNO AND PERMCO
# Then match to GVKEY
os.chdir("C:/Users/Panqiao/Documents/Research/SS - All/SS")
term = ['MFG', 'INTL', 'RLTY', 'LTD']
term_o = ['MANUFACTURING', 'INTERNATIONAL', 'REALTY', 'LIMITED']
term_dict = {'MFG':'MANUFACTURING', 'INTL':'INTERNATIONAL', 'RLTY':'REALTY','LTD':'LIMITED'}
other = ['INC', 'CO', 'CORP']
# O E A INC	OEA
# I P M TECHNOLOGY INC IPM TECHNOLOGY INC

print(os.getcwd())
#First thing to do, collapse DSEnames

#dse_path = "C:/Users/Panqiao/Documents/Research/SS - All/CRSPCOMPSTAT/DSENAMES - small.txt"
crsp_path = "C:/Users/Panqiao/Documents/Research/SS - All/CRSPCOMPSTAT/"
dse_path = "C:/Users/Panqiao/Documents/Research/SS - All/CRSPCOMPSTAT/DSENAMES.txt"
dse_path_s = "C:/Users/Panqiao/Documents/Research/SS - All/CRSPCOMPSTAT/DSE_short.txt"
sec_file_path = "C:/Users/Panqiao/Documents/Research/SS - All/SS/id_file_data.txt"
sec_file_s = "C:/Users/Panqiao/Documents/Research/SS - All/SS/SEC_SHORT.txt"
dse_path_collapsed = 'C:/Users/Panqiao/Documents/Research/SS - All/CRSPCOMPSTAT/DSE_COLLAPSED.txt'
#fhand_sec_online = open("C:/Users/Panqiao/Documents/Research/SS - All/SS/id_file_data.txt", encoding="utf8").splitlines()
#fhand_CRSP_DSE = open("C:/Users/Panqiao/Documents/Research/SS - All/CRSPCOMPSTAT/DSENAMES_small.txt", encoding="utf8")
#for i in fhand_sec_online:
    #print(i)
#fhand_sec_online = csv.reader("C:/Users/Panqiao/Documents/Research/SS - All/SS/id_file_data.txt")
#print(lines)
#sec_online = [x for x in csv.reader(open("C:/Users/Panqiao/Documents/Research/SS - All/SS/id_file_data.txt",'r'),delimiter='\t')]
#print(sec_online)
#df=pd.read_csv('C:/Users/Panqiao/Documents/Research/SS - All/SS/id_file_data.txt', delimiter = '\t')
#df.info()
#fhand_DSE = [x for x in csv.reader(open(dse_path,'r'),delimiter='\t')]
#fhand_SEC = [x for x in csv.reader(open(sec_file_path,'r'),delimiter='\t')]
#print(fhand_DSE)
#compfuncs.write_file(crsp_path, "DSE_SHORT.txt", compfuncs.shorten_file(fhand_DSE), 'w')
#compfuncs.write_file(os.getcwd(), "SEC_SHORT.txt", compfuncs.shorten_file(fhand_SEC),'w')
#reader = csv.reader(open(dse_path,'r'), delimiter='\t')
#fhand_DSE = [next(reader, None)]
#a = [x for x in reader]
#fhand_DSE.extend(a)

#compfuncs.write_file(crsp_path, "DSE_SHORT.txt", compfuncs.shorten_file(compfuncs.prep_file(dse_path)),'w') ##FINAL SHORTENING
#compfuncs.write_file(os.getcwd(), "SEC_SHORT.txt", compfuncs.shorten_file(compfuncs.prep_file(sec_file_path)),'w')

#variables:
#0 - date
#3 - name
#9 - permno
#10 nameendt
#19 permco
#reader = csv.reader(open(dse_path_s,'r'),delimiter='\t')
#reader = csv.reader(open(dse_path,'r'),delimiter='\t')
#file_header, DSE_short  = next(reader, None), [x for x in reader]
#SEC_short = [x for x in csv.reader(open(sec_file_s,'r'),delimiter='\t')]
#compfuncs.pe_list(DSE_short)
#temp = compfuncs.collapse_list(file_header, DSE_short, [3, 9, 19], [0, 3, 6, 8, 9, 10, 19])
#compfuncs.write_file(crsp_path, "DSE_COLLAPSED.txt", temp,'w')

#compfuncs.pe_list(SEC_short)
#print(file_header)

#SEC   0 path	DOC_TYPE	filing_type	filing_type_a	filing_date	document_date	FYE	COMN	ticker	exchange	INCORP	CUSIP	SIC_P	IRS_ID	COMM_NUM	CROSS_REF	doc_number	line_number	AUDITOR

#reader = csv.reader(open(sec_file_s ,'r'),delimiter='\t')
#sec_header, sec_short  = next(reader, None), [x for x in reader]
#print(sec_header)
#compfuncs.pe_list(sec_short)


fhand_DSE = [x for x in csv.reader(open(dse_path_collapsed,'r') , delimiter='\t')][1:]
fhand_SEC = [x for x in csv.reader(open(sec_file_s,'r') , delimiter='\t')][1:]
#compfuncs.match_names(fhand_DSE, fhand_SEC)

#Name variables_DSE
DSE_NAME = [i[1] for i in fhand_DSE]
DSE_TICKER = [i[3] for i in fhand_DSE]
DSE_CUSIP = [i[2] for i in fhand_DSE]
DSE_DATE_1 = [i[0] for i in fhand_DSE]
DSE_DATE_2 = [i[5] for i in fhand_DSE]
DSE_PERMNO = [i[4] for i in fhand_DSE]
DSE_PERMCO = [i[6] for i in fhand_DSE]

#Name variables_SEC
SEC_NAME = [i[7] for i in fhand_SEC]
SEC_TICKER = [i[8] for i in fhand_SEC]
SEC_CUSIP = [i[11] for i in fhand_SEC]
SEC_FDATE = [i[4] for i in fhand_SEC]
SEC_DDATE =[i[5] for i in fhand_SEC]

compfuncs.match_names(SEC_NAME, DSE_NAME)

#print(DSE_NAME)
#print(DSE_TICKER)
#print(DSE_CUSIP)
#print(DSE_DATE_1)
#print(DSE_DATE_2)
#print(DSE_PERMNO)
#print(DSE_PERMCO)
#print(SEC_NAME)
#print(SEC_TICKER)
#print(SEC_CUSIP)
#print(SEC_FDATE)
#print(SEC_DDATE)

#for i in SEC_CUSIP:
    #print(len(i))