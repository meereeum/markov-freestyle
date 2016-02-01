from collections import Counter, defaultdict
import itertools
import sys
import os
import numpy as np

class Riffer():
    def __init__(self, dir_in):
        d_counter = self.parseFiles(dir_in)
        # probability dictionary of markov chain -->
        # word: ( [list,of,next,words], [prob,of,next,words] )
        self.d = {k: ( v.keys(), np.array(v.values(), dtype=np.float32) \
                        / sum(v.itervalues()) ) for k,v in d_counter.iteritems()}


    def parseFiles(self, dir_in):
        d = defaultdict(lambda: Counter())
        for f in os.listdir(dir_in):
            d = self.txt2Markov(d, os.path.join(os.path.abspath(dir_in), f))
        return d


    def txt2Markov(self, d_counter, file_in):
        with open(file_in,'r') as f:
            # TODO: multiple whitespace in a row ?
            words = f.read().strip().lower().split(' ')
        # generalizable n-gram sliding window
        #iterPairs = itertools.izip(*(itertools.islice(words, i, None) for i in xrange(2)))
        iterPairs = ((words[i], words[i+1]) for i in xrange(len(words)-2))
        for w1, w2 in iterPairs:
            d_counter[w1].update([w2])
        return d_counter


    def riff(self, word = None, continue_for = np.inf, accum = []):
        if not word:
            # seed randomly from all words
            word = np.random.choice(self.d.keys())
        choices, probs = self.d[word]
        nxt = np.random.choice(choices, p = probs)
        accum.append(nxt)
        if continue_for:
            try:
                self.riff(nxt, continue_for-1, accum)
            except(RuntimeError):
                pass
        return ' '.join(accum)


#def iterWords(file_in):
    #for line in file_in:
        #for word in line.strip().split():
            #yield word


if __name__ == "__main__":
    try:
        DIR = sys.argv[1]
    except(IndexError):
        DIR = './kendrick'

    x = Riffer(DIR)
    print x.riff(continue_for=100)
