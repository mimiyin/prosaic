import math
import random

class Sine_Wave:
    '''Gradual Growth and Decay'''
    def __init__(self, mod_freq):
        self.x = 0
        self.freq_mult = 0.5
        self.mod_freq = False

        if mod_freq > .5:
            self.modulate = True         

    def run(self): 
        if self.mod_freq: self.freq_mult = math.sin(0.5*self.x) + 1.1
        self.x += 1
        return int(math.sin(self.freq_mult*self.x)*100)


class Tan_Wave:
    ''' Regular pulses and Unpredictable pulses '''
    
    def __init__(self, mod_freq):
        self.x = 0
        self.freq_mult = 0.5
        self.mod_freq = False

        if mod_freq > 0.5: self.mod_freq = True
        else: self.freq_mult = 1

    def run(self):
        if self.mod_freq: self.freq_mult = random.randrange(0, 1000)
        self.x += 1
        return int(math.tan(self.freq_mult*self.x))
    
class Square_Wave:
    ''' Sudden and Sustained Change '''

    def __init__(self, mod_freq):
        self.value = 0
        self.x = 0
        self.hi_period = 10
        self.lo_period = 3
        
        self.up = True
        self.mod_lo = False
        self.mod_hi = False 

        if mod_freq > .67:
            self.mod_lo = True 
            self.modulate_lo = Sine_Wave(0)
        if mod_freq > .33: 
            self.mod_hi = True
            self.modulate_hi = Sine_Wave(0)

    def run(self):
        if self.mod_hi: self.hi_period = self.modulate_hi.run()*0.15 + 16
        if self.mod_lo: self.lo_period = self.modulate_lo.run()*0.05 + 6

        self.x += 1
        
        if self.up and self.x < self.hi_period: self.value = 1
        elif not self.up and self.x < self.lo_period: self.value = -1
        else: 
            self.up = not self.up
            self.x = 0
        return self.value*100

class Saw_Tooth:
    ''' Linear Growth, Sudden Extinction '''

    def __init__(self, mod_freq):
        self.value = -1
        self.x = 0.1
        self.mod_freq = False

        if mod_freq > .5: self.mod_freq = True 

    def run(self): 
        
        if self.value < 1: self.value += self.x
        else: 
            self.value = -1
            if self.mod_freq: self.x = random.random()

    
        return int(self.value*100)
