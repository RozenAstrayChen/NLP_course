import sys

def preprocess(text):
    # preprocess/tokenize the sentence
    processed_data = ...
    return processed_data

def _map(text: str):
    tokens = preprocess(text)

    # [ TODO ] generate the mapper output
    # Output: "{pivot}\t{word}\t{distance}\t{count}"
    # Example: 
    #   predict is  -3  1
    #   predict used    -2  1
    #   predict the -1  1
    #   predict the 1   1
    #   ...
    ...
    
if __name__== "__main__" :
    for line in sys.stdin:
        _map(line)
     