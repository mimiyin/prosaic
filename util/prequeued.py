from django.core.cache import cache
import cPickle as pickle

'''Queue words for poems'''

def prequeue():
    queue = []
    #bookmark = 0
    cache.clear()

    try:
        user_input = raw_input("Enter filename: ")
    except KeyboardInterrupt:
        print '\nInput Error'
        return

    prequeued = open('/Users/hamstar/gitroot/prosaic/static/data/' + user_input + '.txt', 'r')
    
    lines = prequeued.readlines()

    for line in lines:
        queue.append(line)

    print "CACHING!!!"  
    print queue
    
    #cache.set('prequeued', queue, 3600)    
    #cache.set('bookmark', -1, 3600)  
    pickle.dump( queue, open( '/Users/hamstar/gitroot/prosaic/static/data/' + user_input + '.pickle', 'wb' ), pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__': prequeue()