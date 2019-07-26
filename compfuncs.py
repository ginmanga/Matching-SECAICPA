import os, csv


def pe_list(a):
    for i in a:
        print(i)


def remove_abbr(a, b):
    """Removes abbreviations"""
    # b = 0 return list
    # b = 1 return lsit of list
    a_lol = []
    term_dict = {'MFG': 'MANUFACTURING', 'INTL': 'INTERNATIONAL', 'RLTY': 'REALTY', 'LTD': 'LIMITED',
                 'INDS':'INDUSTRIES', 'CO.':'CO', 'CORPORATION':'CORP', 'COS':'COMPANIES', 'COMPANY':'CO'}
    for i in a:
        temp = [term_dict.get(n, n) for n in i.split()]
        if b == 0:
            a_lol.append(" ".join(temp))
        if b == 1:
            a_lol.append([" ".join(temp)])
    return a_lol


def in_match(a):
    """Takes a list and returns index of lists that are still unmatched"""
    count = 0
    indexes = []
    for i in a:
        if not i[1]:
            indexes.append([count])
        count += 1
    return indexes


def eq_name_match(a, b, c):
    """Matches names simply"""
    index_count = 0
    for i in a:
        indices_a = [j for j, elem in enumerate(b) if elem == i[0]]
        if indices_a:
            indices_a.extend([c[indices_a[0]]])
        a[index_count].append(indices_a)
        index_count += 1
    return a


def match_sec_cusip(a, b):
    """Matching cusip"""
    #a List of unmatched indexes with CUSIP
    #b file handler for DSE
    DSE_CUSIP = [i[2] for i in b]
    #indices_a = [j for j, elem in enumerate(b) if elem == i[0]]
    for i in a:
        if len(i[1]) == 9:
            indices_a = [j for j, elem in enumerate(DSE_CUSIP) if elem == i[1][0:len(i[1])-1]]
            #print(indices_a)
        if len(i[1]) == 8:
            if i[1][-1] != '0':
                #print(i)
                #print(i[1][0:7])
                #print('0'+i[1][0:7])
                indices_a = [j for j, elem in enumerate(DSE_CUSIP) if elem == '0'+i[1][0:len(i[1])-1]]
                #print(indices_a )
            if i[1][-1] == '0':
                print(i)
                indices_a = [j for j, elem in enumerate(DSE_CUSIP) if elem == i[1]]
                print(indices_a )
        if len(i[1]) == 7 and i[1]:
            #print(i)
            #print(i[1][-1])
            if i[1][-1] != "1":
                indices_a = [j for j, elem in enumerate(DSE_CUSIP) if elem[0:8] == '00'+i[1][0:len(i[1])-1]]
                print(i)
                #print(i[1][0:7])
                print(indices_a)
            if i[1][-1] == '1':
                #print(i)
                indices_a = [j for j, elem in enumerate(DSE_CUSIP) if elem == i[1]+'0']
                #print(indices_a)
    fc = 0
    for i in DSE_CUSIP:
        #print(i)
        #if i[0:7] == '2942910':
        if fc == 20529:
            print(i)
            print(i[0:7])
        fc += 1


def match_names(a, b, c, d):
    """Take two lists and match on names"""
    a_s = set(a)
    a_rab = remove_abbr(a,1)
    b_rab = remove_abbr(b,0)
    #fm = eq_name_match(a_rab, b_rab, b)
    fmatch = eq_name_match(a_rab, b_rab, b) #initial name match
    index_unmatch = in_match(fmatch) #returns index of unmantchec
    print(fmatch)
    print(index_unmatch)
    index_unmatch_2 = [i+[c[i[0]][11]] for i in index_unmatch] #list of unmatched index + cusip
    match_sec_cusip(index_unmatch_2, d)


    return None#in_match(fm)


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


def shorten_file(file):
    #shortens list
    short_list = []
    for i in file[0:500]:
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

