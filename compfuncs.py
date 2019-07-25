import os, csv


def pe_list(a):
    for i in a:
        print(i)

def eq_name_match(a, b):
    index_count = 0

    for i in a:
        print(i)
        indices_a = [j for j, elem in enumerate(b) if elem == i[0]]
        if indices_a:
            indices_a.extend([b[indices_a[0]]])
        a[index_count].append(indices_a)
        index_count += 1
    return a

def match_names(a , b, x = 0,y = 0):
    """Take two lists and match on names"""
    a_s = set(a)
    a_lol = [[i] for i in a] #turn a into list of lists to accumulate matching data from DSE to SEC
    #b_rep = [i for i in b if ]
    #Look and replace abbraiviations
    #print(a_lol)
    index_count = 0
    fm = eq_name_match(a_lol, b)

    #indices_a = [i for i, item in enumerate(b) if item in a_s]
    print(fm)
    for i in fm:
        if not i[1]:
            print(i)


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
    for i in file[0:200]:
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

