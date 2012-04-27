'''Factory for outputting words web app'''
import datetime

from django.core.cache import cache

class Queue:
    
    def __init__(self):
        '''Queue words for poems'''
        self.queue = []
        self.dump = []
        self.q_idx = 0
        cache.clear()
    
    def run(self, word):
        print "QUEUING " + str(len(self.queue))
        #Go to formulas and retrieve a word
        self.queue.append(word)
        self.dump.append(word)

        if len(self.queue) > 9: 
            cache.set(self.q_idx, self.queue, 30)
            cache.set('bookmark', self.q_idx, 30)
            print "BOOKMARK!!!!!!!! " + str(self.q_idx)
            self.queue = []
            self.q_idx += 1
            if self.q_idx > 9: self.q_idx = 0
        if len(self.dump) > 24: self.write() 
    
    def write(self):
        timestamp = datetime.datetime.now()
        f = open('output/' + str(timestamp) + '.txt', 'w')
        dumplist = '\n'.join(self.dump)
        f.write(dumplist)
        f.close()
        self.dump = []


