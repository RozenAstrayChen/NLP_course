import sys
import os
import pandas as pd
import csv
import re
from signal import signal, SIGPIPE, SIG_DFL, SIG_IGN

def skip_gram(tokens, f_max_dis = 5, p_max_dis = -5):
    token_length = len(tokens)
    
    gram = []

    for idx in range(token_length):
        # pervious
        for i in range(-1, p_max_dis-1, -1):
            if idx+i >= 0:
                gram.append((tokens[idx], tokens[idx+i], i, 1))
        for i in range(1, f_max_dis+1):
            if idx+i < token_length:
                gram.append((tokens[idx], tokens[idx+i], i, 1))

    return gram

def preprocess(text):
    # preprocess/tokenize the sentence
    processed_data = re.sub(r'[^\w\s]',' ',text).lower().split()
    return processed_data

def _map(text: str):
    # [ TODO ] generate the mapper output
    # Output: "{pivot}\t{word}\t{distance}\t{count}"
    # Example: 
    #   predict is  -3  1
    #   predict used    -2  1
    #   predict the -1  1
    #   predict the 1   1
    #   ...
    ...
    tokens = preprocess(text)
    mapper = skip_gram(tokens)
    return mapper
    
if __name__== "__main__" :
    signal(SIGPIPE, SIG_IGN)
    for line in sys.stdin:
        mappers = _map(line)
        #rint(mappers)
        for mapper in mappers:
            print('%s\t%s\t%s\t%s' % (mapper[0], mapper[1], mapper[2], mapper[3]))
        #break # read all file
     