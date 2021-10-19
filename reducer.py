import sys
import os
import pandas as pd
import csv
import re
import ast
from signal import signal, SIGPIPE, SIG_DFL, SIG_IGN

def generate_reducer(reducer_list, skip_list, index=0, overwrite=False):
    if overwrite == False:
        # generate new
        init_list = [skip_list[0], skip_list[1], int(skip_list[3]), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 3..12
        
        if int(skip_list[2])>0:
            init_list[7+int(skip_list[2])] += int(skip_list[3])
        else:
            init_list[8+int(skip_list[2])] += int(skip_list[3])
        #init_list[7+int(skip_list[2])]+=int(skip_list[3]) if int(skip_list[2])>0 else init_list[8+int(skip_list[2])]+=int(skip_list[3])
        reducer_list.append(init_list)
        
    elif overwrite == True:
        reducer_list[index][2] += int(skip_list[3])
        if int(skip_list[2])>0:
            reducer_list[index][7+int(skip_list[2])]+=int(skip_list[3]) 
        else:
            reducer_list[index][8+int(skip_list[2])]+=int(skip_list[3]) 
        #reducer_list[index][7+int(skip_list[2])]+=int(skip_list[3]) if int(skip_list[2])>0 else reducer_list[index][8+int(skip_list[2])]+=int(skip_list[3])
    return reducer_list

if __name__== "__main__" :
    signal(SIGPIPE, SIG_IGN)
    pviot = ''; word ='';reducer_dict = {}; reducer_list = []; index = 0; count=0
    for line in sys.stdin:
        # [ TODO ] collect the output from shuffler and generate reducer output
        # Now you need to calculate the skip-gram frequency with its distance information.
        # Input: 
        #   "{pivot}\t{word}\t{distance}\t{count}"
        # Output: 
        #   "{pivot}\t{word}\t{total_freq}\t{-5}\t{-4}\t{-3}\t{-2}\t{-1}\t{1}\t{2}\t{3}\t{4}\t{5}"
        # Example:
        #   See the sample output file given by TA.
        # Steps: 
        #   1) Parse the input from shuffler
        #   2) Check if this is the same skipgram
        #   3) If so, add the frequency according to its distance
        #   4) If not, output the previous skipgram data
        skip_list = line.strip().split()
        if pviot != skip_list[0]: #pivot not same
            pviot = skip_list[0]; word = skip_list[1]
            reducer_list = generate_reducer(reducer_list, skip_list)
            index += 1

        elif (pviot == skip_list[0]) and (word != skip_list[1]):
            word = skip_list[1]
            reducer_list = generate_reducer(reducer_list, skip_list)
            index += 1          
        elif (pviot == skip_list[0]) and (word == skip_list[1]):
            reducer_list = generate_reducer(reducer_list, skip_list, index-1, True)
        
    for reducer in reducer_list:
        print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s'%(
            reducer[0], reducer[1], reducer[2], reducer[3], 
            reducer[4], reducer[5], reducer[6], reducer[7],
            reducer[8], reducer[9], reducer[10], reducer[11], reducer[12]))
        if not line: continue
        
