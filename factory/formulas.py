import random
import math
import time
import re

from collections import deque
import cPickle as pickle

import weightsoundscore as wss
import wordremix as wrmx

#The "Formula"
import die
import calculator as calc
import voices

import queue
from django.core.cache import cache
import json


def get_input():        
    try:
        user_input = raw_input("Enter a word or a phrase: ")
        form = Formula(user_input)
    except KeyboardInterrupt:
        print '\nInput Error'
        return

class Formula:
    
    def __init__(self, user_input):
        '''Formula for poems'''
        
        # Change up "source of words" here.
        with open('data/commonwords_dict.pickle', 'rb') as c: self.worddict = pickle.load(c)
        with open('data/commonwords_list.pickle', 'rb') as c: self.wordlist = pickle.load(c)
        with open('data/collocations.pickle', 'rb') as c: self.collocations = pickle.load(c)
        with open('data/w5.pickle', 'rb') as p: self.phrases = pickle.load(p)
        
        self.input = user_input
        self.output = self.parse_input(self.input)
        print self.output
        self.output_str = self.get_str()
        self.last_five = deque()
                
        # Pre-calculated ranges for voices, waves and modes
        self.how_many_now = 1
        self.duration = 100
        self.voice_num_ranges = die.roll_die(5)
        print "Num of Voices: " + str(self.voice_num_ranges)
        
        self.mode_ranges = die.build_range_from_values([1, 6, 5, 4, 3, 3, 3]) #die.roll_die(7) 
        print "Modes: " + str(self.mode_ranges)

        self.wave_ranges = die.build_range_from_values([2, 1, 1, 2]) #die.roll_die(4)        
        print "Waves: " + str(self.wave_ranges)

        # A dictionary for each voice
        self.voices = []
        # Create 3 meta-voices for duration, capping, and clipping
        self.meta_voices = [voices.Voice(wave_idx = 0) for i in range(3)]
        
        # Keep track of which voice and mode
        self.winning_voice = 0
        self.winner = 0

        # Start up the Queue for moving outputs int mem-cache       
        self.q = queue.Queue()
        
        # Keep track of whether we're in Manual Mode
        self.manual = False
        self.new_manual = True
        
        # GO !
        self.run()
        
    def listen(self):  
        if self.manual: 
            print "NOT NEW"
            self.new_manual = False
        else: 
            print "NEW MANUAL MODE"
            self.new_manual = True
        
        controls = cache.get('controls')
        print controls
        # Each time the user turns on or off a voice, that gets cached
        # If the status of a voice doesn't change, it doesn't get cached
        # Create / Delete newly added / removed voices
        if controls is not None:
            self.manual = False
            for mode in controls:
                control = int(controls[mode])
                # Is the voice turned on?
                if control == 1: 
                    self.manual = True
                    if self.new_manual:     
                        print "Clear it"
                        self.voices = []
                        self.new_manual = False

                    # Does the voice already exist?
                    voice_doesnt_exist = True
                    print "Hey Hey " + str(len(self.voices))
                    for voice in self.voices: 
                        if voice.mode_idx == int(mode): voice_doesnt_exist = False
                        
                    # Create it if it doesn't exist    
                    if voice_doesnt_exist:
                        print "Hey Now"
                        self.q = ''
                        self.q = queue.Queue()
                        self.voices.append(voices.Voice(wave_ranges = self.wave_ranges, mode_idx = int(mode)))
                elif control == 0:
                    print "No Go"
                    for voice in self.voices: 
                        if voice.mode_idx == int(mode): 
                            self.voices.remove(voice) 
        
    def parse_input(self, inpoot):
        ''' One-time sound score words and phrases against user input '''
        tokens = inpoot.split()
        parsed_input = []
        
        for token in tokens:
            try:
                wdx = self.worddict[token][0]
                parsed_input.append(wdx)  # gram index 
            except: pass
            
        return parsed_input
            
    def dequeue(self):
        ''' Only add to dequeu of words if input is single word '''
        if len(self.output) == 1:
            self.last_five.append(self.output[0])
            if len(self.last_five) < 6:
                return
            else: self.last_five.popleft()
        else: self.last_five.clear()
    
                            
    def run(self):
        time.sleep(1)
        
            
        # Run the meta-voices
        self.meta_voices = calc.kill_or_run(self.meta_voices, False)
        
        # Add missing meta-voices - need 3 at all times
        for i in range(3-len(self.meta_voices)):
            # Duration
            # Cap
            # Clip
            self.meta_voices.append(voices.Voice(wave_idx = 0))

        # Check for manual mode
        self.listen()
        if self.manual:
            print "MANUAL MODE ON!!!"
            self.voices = calc.kill_or_run(self.voices, True)
        else:
            # Run live voices or create some if none are alive
            if(self.how_many_now < 1) : self = calc.add_voices(self)
        
            self.voices = calc.kill_or_run(self.voices, False)
            if len(self.voices) < self.how_many_now: 
                print "Bring out your dead!!!"
                # Sine Wave takes duration cap from 1 to 26
                self.duration = int((self.meta_voices[0].value + 100)*0.125) + 1
                calc.add_voices(self)
        
        
        self.winning_voice = calc.pick_a_winner(self.voices)
        self.winner = self.winning_voice.mode_idx
        
        print "Winner: " + str(self.winner)
        options = []
        if self.winner == 0:
            name = 'Repeat'
            options = self.output
        elif self.winner == 1: 
            name = 'Remix'
            options = wrmx.remix_it(self)
            print options
        elif self.winner == 2: 
            name = 'Stutter'
            options = wss.wordscore_it(self)
        elif self.winner == 3: 
            name = 'Elide'
            options = wrmx.elide_it(self)
        elif self.winner == 4: 
            name = 'Synonymize'
            options = wrmx.synonymize_it(self)
        elif self.winner == 5: 
            name = 'Alliterate'
            options = wss.soundscore_it(self, 0)
        elif self.winner == 6: 
            name = 'Rhyme'
            options = wss.soundscore_it(self, 1)
        
        print "OPTIONS: " + str(options)
        print "WHAT NOW? " + name.upper()
        #print options        
        
        # Sound Parsing
        if self.winner >= 5: self.parse_rhymes(options, self.cap_it(options)) #self.cap_it(options)) 
        else:
            # Build synonym phrase
            if self.winner == 4:
                if len(options) > 0:
                    self.output = []
                    for option in options:
                        try:
                            pick = random.randrange(0, len(option)-1)
                            self.output.extend(option[pick]) 
                        except: continue    
                else: self.output = self.output                                              
            # Stutter and Elide
            elif self.winner > 1: self.output = options[self.cap_it(options)]
            # Repeat and Remix    
            elif self.winner >= 0: self.output = options               
            self.print_it()
            
        self.run()
        
        

    def parse_rhymes(self, options, cap):
        ceiling = int(cap*random.random())
        if ceiling < 1: ceiling = 1
        if ceiling > 7: ceiling = 7
        for i in range(ceiling):
                self.output = options[i]
                self.print_it()
            
    def cap_it(self, options):
        ''' Play with this range to control circularity of poem '''
        peak = len(options)-1
        
        if peak < 5: cap_mult = 1
        else: cap_mult = (self.meta_voices[1].value + 100)*.005
        
        cap = int(cap_mult*peak)
        if cap > peak: cap = peak
        elif cap < 1: cap = 1
        
              
        return random.randrange(0,cap) 

    def get_str(self):
        return (' ').join([self.wordlist[wdx][0] for wdx in self.output])
    
    def cap_eye(self, output):
        ''' Capitalize I's in input '''
        # Look for 'i's inside word boundaries or between word boundary and line break
        return re.sub(r'\bi(\b|\n)', 'I', output) 
    
    def clip_it(self):
        tokens = self.output_str.split()
        # Clip and print the repeat and remixed versions
        max_words = len(tokens)-1
        if max_words > 5 or self.winner < 3:
            print "CLIPPING"
            clip_mult = (self.meta_voices[2].value + 100)*.005
            clip = int(clip_mult*max_words)
            if clip > max_words: clip = max_words
            elif clip < 1: clip = 1
            self.output_str = (' ').join(tokens[0:clip])
        
    def print_it(self):
        
        if type(self.output) is int: self.output = [self.output]
        
        ''' Output and Re-start '''
        # Maintain the running queue
        self.dequeue()    
 
        # Get words
        self.output_str = self.get_str()
        if self.winner < 2 or self.winner == 4: self.clip_it()
        
        print "\n"                
        print "OUTPUT:" + self.output_str.upper()                        
        print "\n\n\n"
             
        # Send word to the word queue with I'd capitalized
        self.q.run(self.cap_eye(self.output_str))
        

  

if __name__ == '__main__': get_input()