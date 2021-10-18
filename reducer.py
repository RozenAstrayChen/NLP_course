import sys

if __name__== "__main__" :

    for line in sys.stdin:
        line = line.strip()
        if not line: continue

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
        ...
