'''Factory for outputting words web app'''
import datetime

from django.core.cache import cache

class Queue:
    
    def __init__(self):
        '''Queue words for poems'''
        cache.clear()

        self.queue = []
        self.dump = []
        self.q_idx = 0
        self.reset_bookmark = False
        self.bookmark = 0
        self.duration = 3600
        cache.set('bookmark', 0, self.duration)
    
    def run(self, word):
        print "QUEUING " + str(len(self.queue))
        #Go to formulas and retrieve a word
        self.queue.append(word)
        self.dump.append(word)
        
        print "RESET BOOKMARK? " + str(self.reset_bookmark)
        

        # As soon as there are 10 items in the queue, write it to the cache
        if len(self.queue) > 9: 
            print "WRITING TO CACHE " + str(self.q_idx)
            cache.set(self.q_idx, self.queue, self.duration)
            
            if self.reset_bookmark:
                # Where can I start from?
                self.bookmark = self.q_idx + 1
                if self.bookmark > 9: self.bookmark = 0
                cache.set('bookmark', self.bookmark, self.duration)
                print "BOOKMARK!!!!!!!! " + str(self.bookmark)
            else: 
                cache.set('bookmark', 0, self.duration)
                print "BOOKMARK!!!!!!!! " + str(self.bookmark)
                
            self.queue = []
            self.q_idx += 1
            if self.q_idx > 9: 
                self.q_idx = 0
                self.reset_bookmark = True
        if len(self.dump) > 24: self.write() 
    
    def write(self):
        timestamp = datetime.datetime.now()
        f = open('output/' + str(timestamp) + '.txt', 'w')
        dumplist = '\n'.join(self.dump)
        f.write(dumplist)
        f.close()
        self.dump = []


