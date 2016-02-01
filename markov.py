from collections import Counter, defaultdict
import itertools
import sys
import os
import string
import numpy as np

class Riffer():
    def __init__(self, file_in):
        self.d = self.txt2Markov(file_in)

    def txt2Markov(self, file_in):
        with open(file_in,'r') as f:
            #iterWords(f)
            # TODO: support for '\n' characters
            #words = f.read().strip().translate(None, string.punctuation).upper().split()
            words = f.read().strip().lower().split()
            n_words = len(words)
        iterPairs = ((words[i], words[i+1]) for i in xrange(n_words-2))
        # generalizable n-gram sliding window
        #iterPairs = itertools.izip(*(itertools.islice(words, i, None) for i in xrange(2)))

        d_counter = defaultdict(lambda: Counter())
        for w1, w2 in iterPairs:
            d_counter[w1].update([w2])

        d_probs = {k: ( v.keys(), np.array(v.values(), dtype=np.float32) \
                        / sum(v.itervalues()) ) for k,v in d_counter.iteritems()}
        return d_probs


    def riff(self, word = None, continue_for = np.inf):
        if not word:
            # seed randomly from all words
            word = np.random.choice(self.d.keys())
        choices, probs = self.d[word]
        nxt = np.random.choice(choices, p = probs)
        print nxt
        if continue_for:
            try:
                self.riff(nxt, continue_for-1)
            except(RuntimeError):
                pass
        return


#def iterWords(file_in):
    #for line in file_in:
        #for word in line.strip().split():
            #yield word


if __name__ == "__main__":
    try:
        FILE = sys.argv[1]
    except(IndexError):
        FILE = './backseat_freestyle.txt'

    x = Riffer(os.path.abspath(FILE))
    x.riff(continue_for=100)
