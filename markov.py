import os

#### read files
# We will be using drama text from Henrik Ibsen, Norway's national poet.
ibs = ""
files_ = os.listdir("C:/Users/alexa/Documents/Personal/Projects/MarkovSyntax/Ibsen")
for f in files_:
    print(f)
    with open("C:/Users/alexa/Documents/Personal/Projects/MarkovSyntax/Ibsen/" + f, "r", encoding="utf-8") as file:
        txt_ = file.read()
        print(len(txt_))
        ibs = ibs + txt_

#### clean text
# Remove non-alphanumeric characters and change to lower case
import re

def clean_text(txt):
    pattern = r'[^a-zA-Z0-9æøåÆØÅ\n]'
    clnd = re.sub(pattern, ' ', txt)
    cldn_txt = ' '.join(clnd.split()).lower()

    return cldn_txt


ibs_c = clean_text(ibs)

#### split n-gram
# define the n-gram size of the markov chain state
def ngram_split(txt, n):
    return ([txt[i:i + n] for i in range(0, len(txt), n)])

ibs_sp = ngram_split(ibs_c, 5)

#### pairs
# store consecutive n-grams
def pairs(lst):
    return list(zip(lst[:-1], lst[1:]))

ibs_p = pairs(ibs_sp)

#### frequency table
# get the probability of moving to the next consecutive n-gram

import pandas as pd
import numpy as np
ibs_np = np.array(ibs_p).reshape(-1, 2)

ibs_np_p = pd.DataFrame(ibs_np, columns=['p1', 'p2'])
freq_ = ibs_np_p.groupby(['p1', 'p2']).value_counts().reset_index()
freq_1 = freq_.groupby('p1').agg({'count' : 'sum'}).reset_index()
freq_1.columns = ['p1', 'count_T']

freq_2 = pd.merge(freq_, freq_1, on = 'p1', how='left')
freq_2['p'] = freq_2['count'] / freq_2['count_T']

#### sample sequence
# finally, build a sequence of tokens of size n and starting from start_w

def build_chain(start_w:str, n:int, seq_ = []):
    if (n <= 0):
        return seq_
    else:
        seq_update = seq_ + [start_w] 
        next_p = freq_2.loc[freq_2.p1 == start_w, 'p']
        next_w = freq_2.loc[freq_2.p1 == start_w, 'p2'] 
        w_choice = np.random.choice(a = next_w, size = 1, replace = False, p = next_p).tolist()[0]       
        return(build_chain(w_choice, n-1, seq_update))


n = 100
start_w = freq_2.sample(1).get('p1').values[0]
word_chain = "".join(build_chain(start_w = start_w, n = n))
print(word_chain)

