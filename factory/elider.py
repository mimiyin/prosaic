import cPickle as pickle 

def build():  
    with open('data/w5_for_collocations.pickle', 'rb') as c: ngrams = list(pickle.load(c))
    #with open('data/w2_for_collocations.pickle', 'rb') as c: ngrams.extend(list(pickle.load(c)))
    with open('data/punctuated_for_collocations.pickle', 'rb') as c: ngrams.extend(list(pickle.load(c)))
    
    print len(ngrams)
     
    by_this = {}
        
    # Go through each line and tally up words that appear next to each other
    for ndx, ngram in enumerate(ngrams):
        print ndx
        for gdx, gram in enumerate(ngram):
            if gdx < len(ngram) - 1:
                this = gram
                that = ngram[gdx+1]
                
                #print this
                #print that
                
                # Is "this" already an entry?
                # Is "that" already an entry?
                # Score this/that combination accordingly
                if this in by_this and that in by_this[this]:
                    by_this[this][that] += 1
                elif this in by_this: by_this[this].update({that: 1})
                else: by_this.update({this : {that : 1}})    
                           
    collocations = []    
    
    # For each anchor word, sort elisions 
    for this, thats in by_this.iteritems():
        sorted_thats = sorted(thats.iteritems(), key = lambda x: x[1], reverse = True)

        just_thats = []
        for thatcount in sorted_thats:
            that = thatcount[0]
            just_thats.append(that)
        
        collocations.append( (this, tuple(just_thats)) )
        #print this
        #print just_thats 
        print len(collocations)                    
    
    pickle.dump( tuple(collocations), open( "data/collocations.pickle", "wb"), pickle.HIGHEST_PROTOCOL)
    print "All Done!"
    return ngrams
    
def get(collocations, last_word):
    words = []
    for thisthats in collocations:
        if thisthats[0] == last_word: words = thisthats[1]
    if len(words) < 1: words = [(last_word)]
    return words


if __name__ == "__main__": build()