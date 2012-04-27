"""
Word Test
"""
import cPickle as pickle

import soundscorer as ss
    
def get_input():    
    try:
        user_input = raw_input("Enter a word: ")
        with open('data/commonwords_dict.pickle', 'rb') as c: commonwords = pickle.load(c)                    
        parsed_input = parse_input(user_input, commonwords)        
        del commonwords
        
        with open('data/commonwords_list.pickle', 'rb') as c: commonwords = pickle.load(c)                    
        ss.soundscore_it(parsed_input, commonwords)
        
    except KeyboardInterrupt:
        print '\nInput Error'
        return    

def parse_input(word, commonwords):
    try:
        # Parse input word
        parsed_input = commonwords[word]
        print parsed_input
    except: 
        print 'Error: Word is not in parsing list: ' + word 
        get_input()
    
    return parsed_input
        
if __name__ == "__main__": get_input()
