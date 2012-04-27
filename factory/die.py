'''Various dice rolling functions to inject semi-randomness into formula.'''

import random

def roll_die(num_options):
    ''' Give it '''
    
    thresholds = []

    add_on = 0    
    # ROLL DICE TO SEE WHICH VOICES GET WHICH THRESHOLDS
    for i in range(num_options):
        value = add_on + random.randrange(0, 100, 1)
        thresholds.append(value)
        add_on = value
    
    return thresholds

def build_range_from_values(values):
    add_on = 0
    for vdx, value in enumerate(values):
        values[vdx] += add_on
        add_on = values[vdx]
    
    return values    

def how_many_to_add(how_many_now, ranges):
    
    # How many voices can I activate max?
    how_many_to_add = len(ranges) - how_many_now
  
    how_many_to_add = pick_one(ranges[:(how_many_to_add-1)])
    return how_many_to_add;


def pick_one(ranges):
    top = max(ranges[0:])
    bottom = min(ranges[0:])-1
        
    # Pick a number within that range
    pick_a_number = random.randrange(bottom, top, 1)
    #print "Chosen Number " + str(pick_a_number)
  
    sieve = ranges[0:]
    # Load a new array of THs with randomly picked number
    sieve.append(pick_a_number)
          
    # Sort it
    sieve.sort()
  
    # The of pick_a_number is the winner
    picked_one = [sdx for sdx, s in enumerate(sieve) if s == pick_a_number]    
    
    return picked_one[0]
