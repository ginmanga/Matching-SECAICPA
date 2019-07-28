import os, csv, copy, time


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
                 'OF':'', 'ASSN':'ASSOCIATION', 'INVS':'INVESTORS', 'CONVERT':'CONVERTIBLE', 'GRW':'GROWTH',
                 'INCM':'INCOME', 'PPTYS':'PROPERTIES', 'MTG':'MORTGAGE', 'TR':'TRUST', 'INCORPORATED':'INC',
                 'L.P.':'LP', 'AMER':'AMERICA'}
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


def in_match(a):
    """Takes a list and returns index of lists that are still unmatched"""
    count = 0
    count_un = 0
    indexes = []
    for i in a:
        if not i[1]:
            indexes.append([count])
            count_un += 1
        count += 1
    print("Unmatched", count_un)
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

#def eq_name_match_2(a, b, c, d):


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


def match_names(a, b, c, d):
    """Take two lists and match on names"""
    #a SEC_NAME
    #b DSE_NAME
    #c fhand_SEC
    #d fhand_DSE
    a_s = set(a)
    a_rab = fix_dsenames(a)
    a_rab = remove_abbr(a_rab, 1)
    b_rab = remove_abbr(b, 0)
    b_rab = fix_dsenames(b_rab)
    #for i in b_rab:
        #print(i)
    fmatch = eq_name_match(a_rab, b_rab, a, b) #initial name match returns list with same dimensions as SEC with DSE match
    #fmatch = eq_name_match(a_rab, b_rab, a, b, options = 1)
    #for i in fmatch:
        #if not i[1]:
            #print(i)
        #print([i[0]])
        #print(i[1])
    #print("JEREEEE")
    #f_match_save = [[i[0]]+i[1] for i in fmatch]
    #for i in f_match_save:
        #print(i)
    ##write_file("C:/Users/Panqiao/Documents/Research/SS - All/temps", "first_match.txt", f_match_save, 'w')

    index_unmatch = in_match(fmatch) #returns index of unmantchec
   #print(index_unmatch)
    index_unmatch_2 = [i+[c[i[0]][11]] for i in index_unmatch] #list of unmatched index + cusip
    fmatch_2 = match_sec_cusip(index_unmatch_2, d, fmatch) # returns new list matched by cusip
    #index_unmatch = in_match(fmatch_2) #remaining unmatched after CUSIP
    index_c = 0
    for i in index_unmatch:
        print(fmatch[i[0]])
        #if not fmatch[index_c][1]:
            #print(fmatch[index_c],i)
        #index_c += 1
        #if not i[1]:
            #print(i)
    #second name match match by name when they do not exactly match
    f_match_save = [[i[0]] + i[1] for i in fmatch_2]
    #write_file("C:/Users/Panqiao/Documents/Research/SS - All/temps", "match_set+cusip.txt", f_match_save, 'w')

    index_unmatch_2 = [i + [c[i[0]][8]] for i in index_unmatch]  #list of unmatched index + ticker
    DSE_TICKER = [i[3] for i in d]

    for i in index_unmatch_2:
        indices_a = ""
        indices_a = [j for j, elem in enumerate(DSE_TICKER) if elem == i[1]]
        try:
            indices_a.append(d[indices_a[0]][1])
        except:
            None
        fmatch_2[i[0]][1].extend(indices_a)
    #print(fmatch_2)
    #print(fmatch_2[25])
    #print(fmatch_2[36])
    #print(index_unmatch)

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

