from django.core.cache import cache

'''Queue words for poems'''
queue = []
bookmark = 0
cache.clear()

def prequeue():
    prequeued = open('output/prequeued1.txt', 'r')
    lines = prequeued.readlines()

    for line in lines:
        queue.append(line)
        
    cache.set(bookmark, queue, 3600)    
    cache.set('bookmark', bookmark, 3600)    

if __name__ == '__main__': prequeue()