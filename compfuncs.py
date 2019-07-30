import os, csv, copy, time, file_prep_funcs


def pe_list(a):
    for i in a:
        print(i)


def remove_abbr(a, b):
    """Removes abbreviations"""
    # b = 0 return list
    # b = 1 return lsit of list
    a_lol = []
    term_dict = {'MFG': 'MANUFACTURING', 'INTL': 'INTERNATIONAL', 'RLTY': 'REALTY', 'LTD': 'LIMITED',
                 'INDS':'INDUSTRIES', 'CO.':'CO', 'CORPORATION':'CORP', 'COS':'COMPANIES', 'COMPANY':'CO',
                 'OF':'', 'ASSN':'ASSOCIATION', 'ASSOC':'ASSOCIATION', 'INVS':'INVESTORS', 'CONVERT':'CONVERTIBLE',
                 'GRW':'GROWTH', 'INCM':'INCOME', 'PPTYS':'PROPERTIES', 'MTG':'MORTGAGE', 'TR':'TRUST',
                 'INCORPORATED':'INC', 'L.P.':'LP', 'AMER':'AMERICA', 'BRDRS':'BREEDERS', 'MGMT': 'MANAGEMENT',
                 'SECS':'SECURITIES', 'ELECTRS':'ELECTRONICS', 'SVCS':'SERVICES', 'TECHS':'TECHNOLOGIES',
                 'ELEC':'ELECTRIC', 'COMPNTS':'COMPONENTS', 'U.S.':'UNITED STATES','US':'UNITED STATES',
                 'TRANSN':'TRANSPORTATION', 'UTILS':'UTILITIES', 'SHS':'SHARES', 'CONV':'CONVERTIBLE',
                 'LABS':'LABORATORIES', 'DEV':'DEVELOPMENT', 'SYS':'SYSTEMS', 'TOB':'TOBACCO', 'CHEM':'CHEMICAL',
                 'HECK S':'HECKS', 'EQUIP':'EQUIPMENT', 'WIS':'WISCONSIN', ',':'', '.':''}
    term_dict_2 = {'L P':'LP'}

    for x, i in enumerate(a):
        if i.find(' L P') != -1 and len(i) - 4 == i.find(' L P'):
            a[x] = i.replace(" L P", " LP")

    for i in a:
        temp = [term_dict.get(n, n) for n in i.split()]
        try:
            temp.remove('')
        except:
            None
        if temp[0] == "THE":
            temp.remove("THE")
        if b == 0:
            a_lol.append(" ".join(temp))
        if b == 1:
            #for j in i:
            a_lol.append([" ".join(temp)])
        #print(a[x])
    return a_lol


def in_match(a, options = 0):
    """Takes a list and returns index of lists that are still unmatched"""
    count = 0
    count_un = 0
    indexes = []
    if options == 0:
        indexes = [[j] for j, elem in enumerate(a) if elem[1] == []]
        print("Unmatched", len(indexes))
    if options == 1:
        indexes = [[j] for j, elem in enumerate(a) if elem[1] != []]
        print("Matched", len(indexes))
    return indexes


def fix_dsenames(a):
    """Fix DSE name like T I I to TII"""
    # print(i)
    # print(temp)
    counter = 0
    accumulator_total = [] #keeps track of index and name changes

    for x, i in enumerate(a):
        list_index = 0
        list_index_a = []
        accumulator = ""
        f = i.split()
        for j in f:
            if len(j) == 1:
                accumulator = accumulator + j
                list_index_a.append(list_index)

            if len(j) > 1 and len(list_index_a) > 1 and list_index_a[0] == 0: # When it is at start of Name

                f = [v for y, v in enumerate(f) if y not in list_index_a]
                accumulator_list = [accumulator]
                accumulator_list.extend(f)
                accumulator_total.append([x, " ".join(accumulator_list)])
                list_index_a = []
            if len(j) > 1 and len(list_index_a) > 1 and list_index_a[0] != 0: # When it is in the middle of Name
                accumulator_list = [accumulator]
                accumulator_list = f[0 : list_index_a[0]] + accumulator_list + f[list_index_a[-1]+1 : ]
                accumulator_total.append([x, " ".join(accumulator_list)])
                list_index_a = []
            list_index += 1
    for i in accumulator_total: # replace names with new names
        a[i[0]] = i[1]
    return a


def eq_name_match(a, b, c, d, options = 0):
    """Matches names simply"""
    c = [[i] for i in c]
    index_count = 0
    #elements = ['CO','LIMITED','LTD','CORP','INCORP','INC','FUND', 'DE', 'CA', 'DEL', 'OLD']
    elements = {'CO', 'LIMITED', 'LTD', 'CORP', 'INCORP', 'INC', 'FUND', 'DE', 'CA', 'OKLA', 'ID'} # elements to discard when matching sets

    for i in a:
        #indices_a = [j for j, elem in enumerate(b) if elem == i[0]]
        indices_a = [str(j) for j, elem in enumerate(b) if elem == i[0]]
        #indices_a = [j for j, elem in enumerate(b) if set(elem.split()) == set(i[0].split())]
        if not indices_a and options == 1:
            indices_a = []
            for j, elem in enumerate(b):

                x = set(elem.split())
                y = set(i[0].split())
                if x == y:
                    indices_a.append(str(j))
                elif x.issubset(y):
                    if y.difference(x).issubset(elements):
                        indices_a.append(str(j))
                elif y.issubset(x):
                    if x.difference(y).issubset(elements):
                        indices_a.append(str(j))
        if indices_a:
            indices_a.extend([d[int(indices_a[0])]])
        c[index_count].append(indices_a)
        index_count += 1
    return c


def eq_name_match_N(a, b, c, d, options = 0):
    """Matches names simply"""
    index_count = 0
    elements = {'CO', 'LIMITED', 'LTD', 'CORP', 'INCORP', 'INC', 'FUND', 'DE', 'CA', 'OKLA', 'ID', 'LP', '&'} # elements to discard when matching sets
    for i in a:
        indices_a = [str(j) for j, elem in enumerate(b) if elem == i[1]]
        if not indices_a and options == 1:
            indices_a = []
            for j, elem in enumerate(b):

                x = set(elem.split())
                y = set(i[1].split())
                if x == y:
                    indices_a.append(str(j))
                elif x.issubset(y):
                    if y.difference(x).issubset(elements):
                        indices_a.append(str(j))
                elif y.issubset(x):
                    if x.difference(y).issubset(elements):
                        indices_a.append(str(j))
        if indices_a:
            indices_a.extend([d[int(indices_a[0])]])
        c[i[0]][1].extend(indices_a)
        index_count += 1
    return c


def eq_name_match_2(a, b, c):
    #a unmatched index and name
    #b matched index and name
    #c fmatched
    count_a = 0
    count_found = 0
    for i in a:
        for j in b:
            if i[1] == j[1]:
                count_found += 1
                print("found one")
                print("This is number:", count_found ,"we have found using this method")
                print(c[i[0]])
                print(c[j[0]])
                c[i[0]][1] = c[j[0]][1]
                break
    print("Total found using the second name method is", count_found)
    return c


def match_sec_cusip(a, b, c):
    """Matching cusip"""
    #a List of unmatched indexes with CUSIP
    #b file handler for DSE
    #c fm master list SEC
    DSE_CUSIP = [i[2] for i in b]
    for i in a:
        indices_a = ""
        if len(i[1]) == 9:
            indices_a = [str(j) for j, elem in enumerate(DSE_CUSIP) if elem == i[1][0:len(i[1])-1]]
            try:
                indices_a.append(b[int(indices_a[0])][1])
            except:
                None
        if len(i[1]) == 8:
            if i[1][-1] != '0':
                indices_a = [str(j) for j, elem in enumerate(DSE_CUSIP) if elem == '0'+i[1][0:len(i[1])-1]]
                try:
                    indices_a.append(b[int(indices_a[0])][1])
                except:
                    None
            if i[1][-1] == '0':
                indices_a = [str(j) for j, elem in enumerate(DSE_CUSIP) if elem == i[1]]
                try:
                    indices_a.append(b[int(indices_a[0])][1])
                except:
                    None
        if len(i[1]) == 7 and i[1]:
            if i[1][-1] not in ["0", "1"]:
                indices_a = [str(j) for j, elem in enumerate(DSE_CUSIP) if elem[0:8] == '00'+i[1][0:len(i[1])-1]]
                try:
                    indices_a.append(b[int(indices_a[0])][1])
                except:
                    None
            if i[1][-1] == '1':
                indices_a = [str(j) for j, elem in enumerate(DSE_CUSIP) if elem == i[1]+'0']
                try:
                    indices_a.append(b[int(indices_a[0])][1])
                except:
                    None
            if i[1][-1] == '0':
                indices_a = [str(j) for j, elem in enumerate(DSE_CUSIP) if elem == '0'+i[1]]
                try:
                    indices_a.append(b[int(indices_a[0])][1])
                except:
                    None
        c[i[0]][1].extend(indices_a)
    return c


def fix_names(a, options=0):
    """Takes a list of names and returns modficied list abbreviations and other problems"""
    #calls remove_abbr and fix_dsenames
    if options == 0:
        #a_rab = fix_dsenames(a)
        #a = remove_abbr(a_rab, 1)
        a = remove_abbr(fix_dsenames(a), 1)
    if options == 1:
        a = fix_dsenames(remove_abbr(a, 0))
    return a


def run_match_1(a, b, c, options=0):
    #a names original
    #b fmatch
    #c variable for matching
    #d source
    if options == 0:
        fmatch = [[i, []] for i in a]
        index_unmatch = [i + [b[i[0]][11]] for i in in_match(fmatch)]  # adds cusip
        fmatch = match_sec_cusip(index_unmatch, c, fmatch)  # match by cusip
        print("Writting temp 1")
        f_match_save = [[i[0]] + i[1] for i in fmatch] # prepare file for writting
        write_file("C:/Users/Panqiao/Documents/Research/SS - All/temps", "temp1.txt", f_match_save, 'w')

    if options == 1:
        fmatch_reader = [x for x in csv.reader(open("C:/Users/Panqiao/Documents/Research/SS - All/temps/temp1.txt", 'r'), delimiter='\t')]
        #print(fmatch_reader)
        #fmatch = [[i[0], i[1]] for i in fmatch]
        fmatch = []
        for i in fmatch_reader:
            #print(len(i))
            #print(i)
            #print(i[0])
            #print(i[1:len(i)])
            fmatch.append([i[0],i[1:len(i)]])
    #print(fmatch)
    return fmatch


def run_match_2(a, b, c, options=0):
    #a names original
    #b names DSE
    #c fmatch
    #d source
    a_rab = fix_names(a)
    if options == 0:
        b_rab = fix_names(b, options=1)
        index_unmatch = [i + a_rab[i[0]] for i in in_match(c)]  # get names of unmatched
        fmatch = eq_name_match_N(index_unmatch, b_rab, c, b, options=1)  # match by name
        print("Writting temp 2")
        f_match_save = [[i[0]] + i[1] for i in fmatch]
        write_file("C:/Users/Panqiao/Documents/Research/SS - All/temps", "temp2.txt", f_match_save, 'w')

    if options == 1:
        fmatch_reader = [x for x in csv.reader(open("C:/Users/Panqiao/Documents/Research/SS - All/temps/temp2.txt", 'r'), delimiter='\t')]
        fmatch = []
        for i in fmatch_reader:
            fmatch.append([i[0],i[1:len(i)]])
    #print(fmatch)
    return fmatch, a_rab


def run_match_self(a, b, options=0):
    # a = a_rab
    # b = fmatch
    if options == 0:
        index_unmatch = in_match(b)
        index_match = in_match(b, options = 1)
        index_unmatch = [i + a[i[0]] for i in in_match(b)]  # get names of unmatched
        index_match = [i + a[i[0]] for i in in_match(b, options = 1)]  # get names of matched
        fmatch = eq_name_match_2(index_unmatch, index_match, b)
        f_match_save = [[i[0]] + i[1] for i in fmatch]
        print("Writting temp 3")
        write_file("C:/Users/Panqiao/Documents/Research/SS - All/temps", "temp3.txt", f_match_save, 'w')
    if options == 1:
        fmatch_reader = [x for x in csv.reader(open("C:/Users/Panqiao/Documents/Research/SS - All/temps/temp3.txt", 'r'), delimiter='\t')]
        fmatch = []
        for i in fmatch_reader:
            fmatch.append([i[0],i[1:len(i)]])
    return fmatch


def finalize_sec(a, b, c, options=0):
    #a SEC_HANDLES
    #b DSE_HANDLE
    #c fmatch
    #names_var = ['path', 'doc_type', 'filing_type', 'filing_type_a', 'filing_date',
                #'document_date','incorp','exchange', 'conm',
                 #,'permco','ticker','DSE_date','DSEe_date', 'permno']
    names_var = ['path', 'doc_type', 'filing_type', 'filing_type_a', 'filing_date',
                'document_date', 'incorp', 'exchange','conm','permco','DSE_date','DSEe_date', 'permno']
    if options == 0:
        DSE_TICKER = [i[3] for i in b]
        DSE_DATE_1 = [i[0] for i in b]
        DSE_DATE_2 = [i[5] for i in b]
        DSE_PERMNO = [i[4] for i in b]
        DSE_PERMCO = [i[6] for i in b]
        SEC_FDATE = file_prep_funcs.conv_dates([i[4] for i in a])
        SEC_DDATE = file_prep_funcs.conv_dates([i[5] for i in a])

        SEC_PATH = [i[0] for i in a]
        SEC_DOC_TYPE = [i[1] for i in a]
        SEC_FILE_TYPE = [i[2] for i in a]
        SEC_FILE_TYPE_a = [i[3] for i in a]
        SEC_INCORP = [i[10] for i in a]
        SEC_EXCH = [i[9] for i in a]

        for i, j in enumerate(c):
            j[0] = [SEC_PATH[i], SEC_DOC_TYPE[i], SEC_FILE_TYPE[i], SEC_FILE_TYPE_a[i],
                    SEC_FDATE[i], SEC_DDATE[i], SEC_INCORP[i], SEC_EXCH[i], j[0]]
            if j[1] and len(j[1]) > 2:
                temp = []
                count_true = 0
                temp_true = []
                temp_false = []
                for x in range(len(j[1])-1): # check if SEC fdate within CRSP Beging and endates
                    temp_1 =[SEC_FDATE[i] >= DSE_DATE_1[int(j[1][x])], SEC_FDATE[i] <= DSE_DATE_2[int(j[1][x])]]
                    temp_2 = [DSE_DATE_1[int(j[1][x])], DSE_DATE_2[int(j[1][x])]]
                    temp.append(temp_2)
                    if temp_1 == [True, True]:
                        temp_true.append(x)
                        count_true += 1
                    else:
                        temp_false.append(x)
                if count_true == 0:
                    #SO FEW HANDLE LATER
                    temp_permco = []
                    for item in temp_false:
                        #print(b[int(j[1][item])])
                        temp_permco.append(b[int(j[1][item])][6])
                    if len(set(temp_permco)) == 1:
                        #print(j)
                        j[1] = [str(list(set(temp_permco))[0]),DSE_DATE_1[int(j[1][0])], DSE_DATE_2[int(j[1][0])],
                                DSE_PERMNO[int(j[1][0])]]
                    if len(set(temp_permco)) > 1:
                        j[1] = ["PMCRSP","", "", ""]
                if count_true > 1:
                    temp_permco = []
                    for item in temp_true:
                        temp_permco.append(b[int(j[1][item])][6])
                    if len(set(temp_permco)) == 1:
                        j[1] = [str(list(set(temp_permco))[0]),DSE_DATE_1[int(j[1][0])], DSE_DATE_2[int(j[1][0])],
                                DSE_PERMNO[int(j[1][0])]]
                    if len(set(temp_permco)) > 1:
                        for item in temp_true:
                            temp_permco.append(b[int(j[1][item])][6])
                if count_true == 1:
                    q = temp_true[0]
                    j[1] = [DSE_PERMCO[int(j[1][0])], DSE_DATE_1[int(j[1][0])], DSE_DATE_2[int(j[1][0])],
                            DSE_PERMNO[int(j[1][0])]]
            if j[1] and len(j[1]) == 2:
                #print(j)
                j[1] = [DSE_PERMCO[int(j[1][0])], DSE_DATE_1[int(j[1][0])], DSE_DATE_2[int(j[1][0])], DSE_PERMNO[int(j[1][0])]]
                print(j)
            if not j[1]:
                j[1] = ["", "", "", ""]
        fmatch = c
        f_match_save = [i[0] + i[1] for i in c]
        print("Writting temp 4")
        write_file("C:/Users/Panqiao/Documents/Research/SS - All/temps", "temp4.txt", f_match_save, 'w')

    if options == 1:
        fmatch_reader = [x for x in csv.reader(open("C:/Users/Panqiao/Documents/Research/SS - All/temps/temp4.txt", 'r'), delimiter='\t')]
        fmatch = []
        for i in fmatch_reader:
            #fmatch.append([i[0], i[1:len(i)]])
            fmatch.append(i)

    return fmatch

    #for i in c:
        #print(i)




def match_names(a, b, c, d):
    """Take two lists and match on names"""
    #a SEC_NAME
    #b DSE_NAME
    #c fhand_SEC
    #d fhand_DSE

    #a_rab = fix_names(a)
    #b_rab = fix_names(b, options=1)

    #fmatch = [[i,[]] for i in a]
    #index_unmatch = [i + [c[i[0]][11]] for i in in_match(fmatch)] #adds cusip
    #fmatch = match_sec_cusip(index_unmatch, d, fmatch) #match by cusip
    #print("Writting temp 1")
    #f_match_save = [[i[0]] + i[1] for i in fmatch] # prepare file for writting
    #write_file("C:/Users/Panqiao/Documents/Research/SS - All/temps", "temp1.txt", f_match_save, 'w')

    #fmatch = run_match_1(a, c, d, options=1)
    #fmatch, a_rab = run_match_2(a, b, fmatch, options=1)
    #fmatch = [[i, []] for i in a]
    #a_rab = fix_names(a)
    #fmatch = run_match_self(a_rab, fmatch, options=1)
    #print(fmatch[0])
    fmatch = [[i, []] for i in a]
    fmatch = finalize_sec(c, d, fmatch, options=1) #to print and match with gvkey
    #print(fmatch[0])
    #for i in fmatch:
        #print(i)
    # Need to mathc to gvkey.
    crsp_comp = 'C:/Users/Panqiao/Documents/Research/SS - All/CRSPCOMPSTAT/CRSPCOMPSTATLINK.csv'
    fhand_CRPCM = [x for x in csv.reader(open(crsp_comp, 'r'), delimiter=',')][1:]
    #for i in fhand_CRPCM:
        #print(i)
    #print(fmatch[0])
    #print(fmatch[0][9])
    #fmatch permco is 9
    #fhand_CRPPCM 0 is gvkey 9 is permco
    #print(fhand_CRPCM[0][9])
    names_var_final = ['gvkey', 'filing_type', 'document_date', 'permco',
                       'incorp', 'exchange', 'conm_sec', 'filing_date',
                       'file_a', 'sec_doc', 'sec_path']


        #['path', 'doc_type', 'filing_type', 'filing_type_a', 'filing_date',
         #        'document_date', 'incorp', 'exchange', 'conm', 'permco', 'DSE_date', 'DSEe_date', 'permno']
    for i, item in enumerate(fmatch):
        #new list gvkey
        #gvkey = []
        gvkey = [[] for i in a]
        matches = []
        if not item[9]: #no permno
            gvkey[i] = ["", fmatch[i][2], fmatch[i][5], fmatch[i][9]
                       ,fmatch[i][6], fmatch[i][7] ,fmatch[i][8], fmatch[i][4]
                       ,fmatch[i][3], fmatch[i][1], fmatch[i][0]]

        if item[9]: #have permno
            indices_a = [j for j, elem in enumerate(fhand_CRPCM) if elem[9] == item[9]]
            if len(indices_a) == 1: #only one permno match
                gvkey[i] = [fhand_CRPCM[indices_a[0]][0], fmatch[i][2], fmatch[i][5], fmatch[i][9],
                            fmatch[i][6], fmatch[i][7], fmatch[i][8], fmatch[i][4],
                            fmatch[i][3], fmatch[i][1], fmatch[i][0]]
            if len(indices_a) > 1: #multiple permno match, pick one that has correct dates
                gvkey_ac = []
                for x in indices_a:
                    gvkey_ac.append(fhand_CRPCM[x][0])
                if len(set(gvkey_ac)) == 1:
                    gvkey[i] = [list(set(gvkey_ac))[0], fmatch[i][2], fmatch[i][5], fmatch[i][9],
                                fmatch[i][6], fmatch[i][7], fmatch[i][8], fmatch[i][4],
                                fmatch[i][3], fmatch[i][1], fmatch[i][0]]
                if len(set(gvkey_ac)) > 1:
                    indexe_t = []
                    for x in indices_a:
                        if (fhand_CRPCM[x][11]>=item[4]>=fhand_CRPCM[x][10]):
                            indexe_t.append(x)
                    if len(set(indexe_t)) == 1:
                        gvkey[i] = [fhand_CRPCM[indexe_t[0]][0], fmatch[i][2], fmatch[i][5], fmatch[i][9],
                                    fmatch[i][6], fmatch[i][7], fmatch[i][8], fmatch[i][4],
                                    fmatch[i][3], fmatch[i][1], fmatch[i][0]]
                    if len(set(indexe_t)) > 1:
                        gvkey[i] = ["", fmatch[i][2], fmatch[i][5], fmatch[i][9],
                                    fmatch[i][6], fmatch[i][7], fmatch[i][8], fmatch[i][4],
                                    fmatch[i][3], fmatch[i][1], fmatch[i][0]]
                        # Not many, no need to worry about it now
                        #print("MORETANONE")
                        #print(item)
                        #print(indexe_t)
                        None
                    if len(set(indexe_t)) == 0:
                        gvkey[i] = ["", fmatch[i][2], fmatch[i][5], fmatch[i][9],
                                    fmatch[i][6], fmatch[i][7], fmatch[i][8], fmatch[i][4],
                                    fmatch[i][3], fmatch[i][1], fmatch[i][0]]
                        #Not many, no need to worry about it now
                            #print(fhand_CRPCM[x])
                        None
        #print(gvkey[i])
    #print(sec + gvkeuy to file


    names_var = ['path', 'doc_type', 'filing_type', 'filing_type_a', 'filing_date',
                'document_date', 'incorp', 'exchange','conm', 'permco','DSE_date','DSEe_date', 'permno']

    sec_final = 'C:/Users/Panqiao/Documents/Research/SS - All/Final'
    write_file(sec_final, 'sec_gvkey', gvkey, 'w')






    return None


def collapse_list(header, a, x, y):
    #a list to collapse
    #x group of variables used to collapase, indexes
    #y list of columns to keep
    # a collapsed list collpased, date from the first row and rest from the last
    counter_1 = 0
    counter_2 = 0
    accumulator_text = []
    accumulator_list = []
    collapsed_list = [[header[i] for i in y]]
    for i in range(len(a)):

        if counter_2 == 0:

            accumulator_text.append([a[i][ii] for ii in x])
            accumulator_list.append([a[i][iii] for iii in y])

        if counter_2 > 0:

            list_to_check = [a[i][ii] for ii in x]
            list_to_accumulate = [a[i][iii] for iii in y]
            if list_to_check == accumulator_text[-1]:
                accumulator_text.append([a[i][ii] for ii in x])
                accumulator_list.append([a[i][iii] for iii in y])

            if list_to_check != accumulator_text[-1]:

                collapse_accumulator = [accumulator_list[0][0]]
                collapse_accumulator.extend(accumulator_list[-1][1:])
                collapsed_list.append(collapse_accumulator)
                accumulator_text = [list_to_check]
                accumulator_list = [list_to_accumulate]

        counter_2 += 1

    return collapsed_list


def prep_file(path):
    #reads text file and with header....
    reader = csv.reader(open(path, 'r'), delimiter='\t')
    file_w_header = [next(reader, None)]
    a = [x for x in reader]
    file_w_header.extend(a)
    return file_w_header


def shorten_file(file, size):
    #shortens list
    short_list = []
    for i in file[0:size]:
        print(i)
        short_list.append(i)
    return short_list


def write_file(path_file, filename, data, write_type):
    """Writes all data to file"""
    #first tells if it writtes or appends
    #write_type 'w' or 'a'
    #print(data)
    path_to_2 = os.path.join(path_file, filename)
    with open(path_to_2, write_type) as file:
        file.writelines('\t'.join(i) + '\n' for i in data)
    file.close()

