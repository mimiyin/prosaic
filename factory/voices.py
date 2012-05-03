'''Voice class'''

import random

import waves
import die

def add_voices(how_many_to_add, duration, mode_ranges, wave_ranges):
    # Create voices
    # Store values for color, whether to modulate frequency, duration, duration counter and curve type
    return [Voice(duration = duration, mode_ranges = mode_ranges, wave_ranges = wave_ranges, mode_idx = -1) for i in range(how_many_to_add)]

def create_wave(wave_idx, mod_freq):
            # Store curve
        if wave_idx == 0:
            return waves.Sine_Wave(mod_freq) 
        elif wave_idx == 1:
            return waves.Tan_Wave(mod_freq) 
        elif wave_idx == 2:
            return waves.Square_Wave(mod_freq) 
        elif wave_idx == 3:
            return waves.Saw_Tooth(mod_freq) 
        
class Voice:
    '''Tell the voice:
       Are we in manual mode?
       Manual mode values
       Mode Ranges
       Wave Ranges 
    '''
    def __init__(self, duration = 10, mode_ranges = [], wave_ranges = [], mode_idx=-1, mod_freq=-1, wave_idx=-1):
        self.value = 0
        
        # Select a Mode only if there are mode_ranges to select from
        if mode_idx > -1: self.mode_idx = mode_idx
        elif len(mode_ranges) > 0: self.mode_idx = die.pick_one(mode_ranges)
        else: self.mode_idx = -1
        
        # Create Sub-Waves
        # Remix/Repeat: Up to 10
        if self.mode_idx == 0 or self.mode_idx == 1: cap = 10
        # Stutter: 3 options
        elif self.mode_idx == 2: cap =3
        # Elision: 2 options
        elif self.mode_idx == 3 : cap = 2
        # Allit/Rhyme: 1 option
        elif self.mode_idx >= 5: cap = 1
        # Synonymize does not have cap
        else: cap = 0
        
        self.sub_waves_idxes = [die.pick_one(wave_ranges) for i in range(cap)]
        self.sub_waves = [create_wave(idx, random.random()) for idx in self.sub_waves_idxes]

        
        # Modulate Frequency?
        if mod_freq > -1: self.mod_freq = mod_freq
        else: self.mod_freq = random.random()
        
        # Which Wave Function?
        if wave_idx > -1: self.wave_idx = wave_idx
        else: self.wave_idx = die.pick_one(wave_ranges)
                
        # Get the Wave Object
        self.wave = create_wave(self.wave_idx, self.mod_freq)
        
        # Pick a Duration
        self.duration = random.randrange(0, duration, 1)
        # Kick off Duration counter for each voice
        self.counter = 0
    
        print "Mode:" + str(self.mode_idx) + "\tMod Freq:" + str(self.mod_freq) + "\tDuration:" + str(self.duration) + "\tWhich Curve:" + str(self.wave_idx)   