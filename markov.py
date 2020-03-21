from collections import Counter, defaultdict
# import itertools
import sys
import os
import numpy as np


class Riffer():
    def __init__(self, dir_in, newline_chars=True):
        self.spliton = (' ' if newline_chars else None) # split defaults to whitespace
        d_counter = self.parseFiles(dir_in)

        # probability dictionary of markov chain -->
        # word: ( [list,of,next,words], [prob,of,next,words] )
        self.d = {k: ( v.keys(), (np.array(v.values(), dtype=np.float32)
                                  / sum(v.values())) )
                  for k,v in d_counter.items()}


    def parseFiles(self, dir_in):
        d = defaultdict(lambda: Counter())
        # depth = 1
        # dirname, subdirs, files = os.walk(os.path.abspath(dir_in)).next()
        for root, dirs, files in os.walk(os.path.abspath(dir_in)):
            for filepath in (os.path.join(root, f) for f in files):
                d = self.txt2Markov(d, filepath) # update d_counter
        return d


    def txt2Markov(self, d_counter, file_in):
        with open(file_in,'r') as f:
            # TODO: multiple whitespace in a row ?
            words = f.read().strip().lower().split(self.spliton)

        # generalizable n-gram sliding window
        # for w1, w2 in zip(*(itertools.islice(words, i, None) for i in range(2))):

        for w1, w2 in zip(words, words[1:]):
            d_counter[w1].update([w2])

        return d_counter


    def freestyle(self, word=None, continue_for=np.inf, accum=[]):
        if not word: # seed randomly from all words
            word = np.random.choice(self.d.keys())

        try:
            choices, probs = self.d[word]
            nxt = np.random.choice(choices, p=probs)
        except(KeyError):
            # why does this happen ?
            print(f'uh oh: {word}')
            import IPython; IPython.embed()

        accum.append(nxt)

        if continue_for:
            try:
                self.freestyle(nxt, continue_for - 1, accum)
            except(RuntimeError):
                pass

        return ' '.join(accum)


# def iterWords(file_in):
#     for line in file_in:
#         for word in line.strip().split():
#             yield word


if __name__ == "__main__":
    try:
        DIR = sys.argv[1]
    except(IndexError):
        DIR = './kendrick'

    x = Riffer(DIR)
    print(x.freestyle())
    #print(x.freestyle(continue_for=100))
