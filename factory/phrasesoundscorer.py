"""
Parse Phrases for Sounds
"""
import nltk
import cPickle as pickle


#for sound processing
import soundscorer as ss
import ngrams as ng

def get_input():
        
    try:
        user_input = raw_input("Enter a phrase: ")
        with open('data/commonwords_dict.pickle', 'rb') as c: commonwords_dict = pickle.load(c)                    
        parsed_input = parse_input(user_input, commonwords_dict)
        del commonwords_dict
        
        with open('data/w4.pickle', 'rb') as n: ngrams = pickle.load(n)
        print ngrams[0]
        # Score ngrams against input phrase
        ss.soundscore_it(parsed_input, ngrams)        

    except KeyboardInterrupt:
        #print '\nInput Error'
        return

def parse_input(user_input, commonwords):
    
    # Split out input phrase into individual words
    grams = nltk.word_tokenize(user_input.lower())
    parsed_input = ng.parse_ngram(grams, commonwords)
    print parsed_input
    return parsed_input

              
if __name__ == "__main__":get_input()
