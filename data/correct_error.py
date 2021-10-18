from collections import Counter, defaultdict
import math, re
import kenlm
import operator
import itertools
import ipdb

model = kenlm.Model('bnc.prune.arpa')

def words(text): return re.findall(r'\w+|[,.?]', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return float(WORDS[word] / N)


def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)


def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def suggest(word):
    '''return top 5 words as suggestion, original_word as top1 when original_word is correct'''
    suggest_P = {}
    edits_set = edits1(word).union(set(edits2(word)))
    for candidate in known(edits_set):
        suggest_P[candidate] = P(candidate)
    if word in WORDS:
        suggest_P[word] = 1
    suggest_can = sorted(suggest_P, key=suggest_P.get, reverse=True)[:5]
    
    return suggest_can

import itertools
def generate_candidate(candidate_of_token, candidate, g_s, i):
    if i == len(candidate_of_token):
        candidate.append(g_s)
        return
    for token in candidate_of_token[i]:
        if i == 0:
            generate_candidate(candidate_of_token, candidate, token, i+1)
        else:
            if token is "":
                generate_candidate(candidate_of_token, candidate, g_s+token, i+1)
            else:
                generate_candidate(candidate_of_token, candidate, g_s+' '+token, i+1)
    
def find_best_candidate(candidates):
    best_candidate = ''; best_score = -1000
    for candidate in candidates:
        score = model.score(candidate, bos=True, eos=True)/len(candidate)
        if score > best_score:
            best_score = score
            best_candidate = candidate

    return best_candidate

    ###### Task1 ######
def spelling_check(sentence):
    sentence = sentence.split()
    candidates = []
    ## TODO ##
    known_toekn = known(sentence)
    # if sentence of token not found in know that will change to suggest token
    for i in range(0, len(sentence)):
        if sentence[i] not in known_toekn:
            sentence[i] = suggest(sentence[i])
        else:
            sentence[i] = [sentence[i]]
    # generate candidate
    generate_candidate(sentence, candidates, '', 0)
     
    return find_best_candidate(candidates), candidates



print("Task 1 Spelling Check")
task1_input = 'he sold everythin escept the housee'
#task1_input = 'nobady knows thats thing'
print("Text:",task1_input,"\n")
print("Candidates:")
task1_result, task1_candidate = spelling_check(task1_input)

for i in task1_candidate[:30]:
    print(i)
print("Number of Candidate:", len(task1_candidate))
print()
print("Result:", task1_result, "\n\n\n")
ipdb.set_trace()


###### Task2 ######a

atcs = {"", "the", "a", "an"}
preps = {"", "about", "at", "by", "for", "from", "in", "of", "on", "to", "with"}

def prep_check(sentence):
    sentence = sentence.split()
    candidates = []; best_candidate = ''
    ## TODO #
    for i in range(0, len(sentence)):
        if sentence[i] in atcs:
            sentence[i] = list(atcs)
        elif sentence[i] in preps:
            sentence[i] = list(preps)
        else:
            sentence[i] = [sentence[i]]

    generate_candidate(sentence, candidates, '', 0)
    
    
    return find_best_candidate(candidates), candidates


print("Task 2 Preposition and Article Check")
task2_input = 'look on an picture in the right'
#task2_input = 'at an afternoon'
print("Text:",task2_input,"\n")
task2_result, task2_candidate = prep_check(task2_input)
print("Candidates:")
for i in task2_candidate[:30]:
    print(i)
print("Number of Candidate:", len(task2_candidate))
print()
print("Result:", task2_result,"\n\n\n")
ipdb.set_trace()

def process_sent(sent):
    ## TODO ##
    candidate1,_ = spelling_check(sent)
    candidate2,_ = prep_check(candidate1)
    return candidate2


print("Task 3 Combination")
task3_input = 'we descuss a possible meamin by that'
print("Text:",task3_input,"\n")
comb_result = process_sent(task3_input)
print("Result:", comb_result)
ipdb.set_trace()
