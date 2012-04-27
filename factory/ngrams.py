"""
Create new phoneme list by matching against commonwords list
"""
import cPickle as pickle
import re

def run():
    fileloc = get_input()
    find_filename = re.findall(r'/\w+\.', fileloc)[0]
    strip_filename = find_filename[1:]
    filename = strip_filename[:-1]
    try:
        ngrams = load_ngrams(fileloc)
    except:
        print "Captan Mimi ! Mission has failed."
        run()    
    
    with open('data/commonwords_dict.pickle', 'rb') as c: commonwords_dict = pickle.load(c)                    
    parsed_ngrams = parse_ngrams(ngrams, commonwords_dict)
    for parsed_ngram in parsed_ngrams: 
        if type(parsed_ngram[0]) is str: print parsed_ngram
    print parsed_ngrams[0] 
    pickle_it(parsed_ngrams, filename)
    
# Enter ngram file to parse    
def get_input():
        
    try:
        fileloc = raw_input("Enter a file path: ")
        return fileloc
    except KeyboardInterrupt:
        print '\nInput Error'
        
# Process most common wordlist
def load_ngrams(fileloc):  
    ngrams = []
    ngrams_to_parse = open(fileloc, 'r')
    ngrams_to_parse = ngrams_to_parse.readlines()
    for idx, line in enumerate(ngrams_to_parse):
        #if idx % 2 == 0:
        entry = line.split()
        grams = entry[1:]
        ngram = cleaned_up((' ').join(grams))
        if ngram is not None:
            clean_grams = ngram.split()
            ngrams.append([clean_grams, int(entry[0])])
        #else: pass    
    print len(ngrams)    
    return ngrams

def cleaned_up(ngram):
    # Get rid of gap before contraction
    # If ngram begins with contraction, turn it into full-word
    #regram = re.sub('\sn\'t', 'n\'t', ngram)
        
    #regram = re.sub('^n\'t', 'not', regram)
#    regram = re.sub('\s\'ve', '\'ve', regram)
#    regram = re.sub('^\'ve', '\'ve', regram)
#    regram = re.sub('\s\'s', '\'s', regram)
#    regram = re.sub('^\'s', 'is', regram)
    
    # Check for composite words
    regram = re.sub('[/\-_]', ' ', ngram)
    
    # Lower I
    regram = re.sub('\bI\b', 'i', regram)
    
    # Check for periods, parentheses and capital letters, those entries should be removed
    match = re.search('[\.()A-Z]', regram)
    if match: regram = None
    return regram
        

def parse_ngrams(ngrams, commonwords): 
    counter = 0
    parsed_ngrams = []
    
    # Get pronunciations for all the words in each ngram          
    for ndx, ngram in enumerate(ngrams): 
        #parsed_ngram = parse_ngram(ngram, commonwords)
        parsed_ngram = parse_ngram_for_collocations(ngram, commonwords)  
        if parsed_ngram is not None: 
            parsed_ngrams.append(parsed_ngram)
        
    return tuple(parsed_ngrams)

def parse_ngram(ngram, commonwords):
    parsed_ngram = [[], 0, [], [], [], 0]
        
    for gram in ngram[0]:   # look through list of grams in ngram        
        try:
            parsed_gram = commonwords[gram]
            parsed_ngram[0].append(parsed_gram[0])  # gram index 
            parsed_ngram[2].extend(parsed_gram[2])  # phs  
            parsed_ngram[4].extend(parsed_gram[4])  # stresses 
            parsed_ngram[5] += parsed_gram[5]       # sylls
        except:
            if len(parsed_ngram[0]) > 1: break
            else: return None
            
    # Create reversed ngram phs        
    parsed_ngram[3] = parsed_ngram[2][0:]
    parsed_ngram[3].reverse()

    parsed_ngram[0] = tuple(parsed_ngram[0]) 
    parsed_ngram[2] = tuple(parsed_ngram[2])
    parsed_ngram[3] = tuple(parsed_ngram[3])  
    parsed_ngram[4] = tuple(parsed_ngram[4])  
       
    parsed_ngram[1] = ngram[1]                      # transfer freq score
      
    #print parsed_ngram
    
    return tuple(parsed_ngram) 

def parse_ngram_for_collocations(ngram, commonwords):
    parsed_ngram = []
        
    for gram in ngram[0]:   # look through list of grams in ngram        
        try:
            parsed_gram = commonwords[gram]
            parsed_ngram.append(parsed_gram[0])  # gram index 
        except:
            if len(parsed_ngram) > 1: break
            else: return None
      
    #print parsed_ngram
    
    return tuple(parsed_ngram) 

def pickle_it(ngrams, filename): 
    pickle_filepath = "data/"+  filename +'_for_collocations.pickle'
    pickle.dump( ngrams, open( pickle_filepath, "wb"), pickle.HIGHEST_PROTOCOL)
    print "All Done!"
    
if __name__ == "__main__": run()
