"""
Clean words from commonwords list. Find mispelled words. Words with punctuation.
To create secondary word lists to be re-filtered or curated by hand.
"""
import nltk
import re
from nltk.corpus import *

import operator
import cPickle as pickle

import soundparser as sp



# Process most common wordlist
def parse_common_words():
    worddict = {}
    wordlist = open('data/500K_WORDS.txt', 'r')
    wordlist = wordlist.readlines()

    for line in wordlist:
        tokens = line.split()
        word = tokens[1]
        if word not in worddict:
            worddict[word] = {'word': word, 'freq': int(tokens[0]), 'pos': tokens[2]}
    
    print len(worddict)
    return worddict    

def punctuated(word):
    
    pattern = '^\''
    match = re.search(pattern, word)
    if match: return False

    # Get rid of words with periods and parentheses
    pattern = '[\.()]'
    match = re.search(pattern, word)
    if match: return False
    
    # Keep compound words
    pattern = '[/\-_]'
    match = re.subn(pattern, ' ', word)
    if match[1] > 0: return match[0]
    else: return True
           
def match_common_words():
    w = open('data/commonwords.txt', 'w')
    s = open('data/shortwords.txt', 'w')
    p = open('data/punctuated.txt', 'w')
    m = open('data/mispelled.txt', 'w')

    mispells = []
    punctuates = []
    sper = sp.SoundParser()

    worddict = parse_common_words() 
    commonwords_list = []
    commonwords_dict = {}
    
    #Look through all the words in the phoneme list
    for word in worddict:

        # Extract the words that have punctuation in them
        depuncted = punctuated(word)
        print depuncted
        if type(depuncted) is str:
            p.write(str(worddict[word]['freq']) + '\t' + depuncted + '\t' + worddict[word]['pos'] + '\n')
            punctuates.append(depuncted)
        elif depuncted is False:
                m.write(word + '\n')
                mispells.append(word)
        elif depuncted is True: 
            # Send the word to the nltk pronunciation dictionary   
            parsed_word = sper.parse_word(word)
            if parsed_word is not False:
                if len(word) < 4:
                    s.write(str(worddict[word]['freq']) + '\t' + word + '\t' + worddict[word]['pos'] + '\n')
                else:
                    w.write(str(worddict[word]['freq']) + '\t' + word + '\t' + worddict[word]['pos'] + '\n')
                
                ''' Create list and dict of words '''    
                list_entry = list(parsed_word[0:])
                list_entry.insert(0, word)                      # put the word in text at the end of the list
                list_entry.insert(1, worddict[word]['freq'])    # insert the freq score of the word at the front of the list
                commonwords_list.append( tuple(list_entry) )                

                
                dict_entry = list(parsed_word[0:])
                dict_entry.insert(0, len(commonwords_list)-1)   # insert idx of the word
                dict_entry.insert(1, worddict[word]['freq'])    # insert freq score of the word
                commonwords_dict[word] = tuple(dict_entry)                

                    
    w.close()
    s.close()                 
    p.close()
    m.close()               
    pickle_it(tuple(commonwords_list), suffix = '_list')
    pickle_it(commonwords_dict, suffix = '_dict')
    print len(commonwords_list)
    
def pickle_it(commonwords, suffix = ''):    
    pickle.dump( commonwords, open( "data/commonwords" + suffix + ".pickle", "wb" ), pickle.HIGHEST_PROTOCOL)
    print "All Done!"
    
if __name__ == "__main__":match_common_words()
