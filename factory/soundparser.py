'''
Performs sound analysis on individual words. 
Returns a dictionary of analyses.
'''

import re
import nltk
import cPickle as pickle

class SoundParser():
    def __init__(self):
        # Build phonemes from scratch
        self.cmudict = nltk.corpus.cmudict.dict() 
        self.phonemes = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'B', 'CH', 'D', 'DH', 'EH', 'ER', 'EY', 'F', 'G', 'HH', 'IH', 'IY', 'JH', 'K', 'L', 'M', 'N', 'NG', 'OW', 'OY', 'P', 'R', 'S', 'SH', 'T', 'TH', 'UH', 'UW', 'V', 'W', 'Y', 'Z', 'ZH']
        self.ph_dict = {}
        
        # Translate phoneme strings into ints        
        for phdx, phoneme in enumerate(self.phonemes):
            self.ph_dict[phoneme] = phdx
        
    def parse_word(self, word):
        try:                                       
            pron = self.cmudict[word][0]
            phs = self.find_phs(pron)
            reverse = self.reverse(phs)
            stresses = self.find_stresses(pron)
            sylls = self.count_syllables(pron)
            parsed_word = tuple([phs, reverse, stresses, sylls])
            return parsed_word
        except: 
            return False        

        
    def find_phs(self, pron):
        phs = []
        for pr in pron:
            ph = self.ph_dict[re.sub("\d", "", pr)]  
            phs.append(ph)
        return tuple(phs)
        
    def reverse(self, whatever):
        reverse = list(whatever[0:])
        reverse.reverse()
        return tuple(reverse)
        
    def find_stresses(self, pron):
        stresses = []
        for ph in pron:
            stress = re.sub("[A-Za-z]", "", ph)
            if stress:
                stresses.append(int(stress))
        return tuple(stresses)
         
    def count_syllables(self, pron):
        syllable_count = len([x for x in list(''.join(pron)) if x >= '0' and x <= '9'])
        return syllable_count
