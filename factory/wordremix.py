import random
import re

import synonymizer as syn
import elider as el

import die

def synonymize_it(form):
    ''' Find synonyms or antonyms ''' 
                 
    synset = []
    synsets = []
    possible_wdxes = []
    
    # Get the strings of the output
    strings = form.output_str.split()
                      
    for wdx, word in enumerate(strings):
        # Only look for synonyms of words with more than 2 letters
        if len(word) > 2:
            possible_wdxes.append(wdx)
    
    total_poss = len(possible_wdxes)                      
    if total_poss > 0:
        for i in range(total_poss):
            # Of the possible words to replace, chose one at random
            wdx = possible_wdxes[random.randrange(0, len(possible_wdxes))]
            
            # Go get synonyms and antonyms
            syns_n_ants = syn.get(strings[wdx])
            
            # Always use antonyms if there are any
            synset = syns_n_ants['antonyms']
            synset.extend(syns_n_ants['synonyms'])
            
            if len(synset) > 0:
                print synset
                numbers = []
                for entry in synset:
                    number = form.parse_input(re.sub('[/\-_]', ' ', entry))
                    if len(number) > 0: numbers.append(number) 
                synsets.append(numbers)  
    print synsets
        
    return synsets 
              
def elide_it(form):
    ''' Find collocations, vary whether to return just the 2nd or both words ''' 
     
    tokens = form.output[0:]      
    this = tokens[-1]
    thats = el.get(form.collocations, this)
    
    # Calculate probably of returning one or two-word elision
    values = [wave.run() for wave in form.winning_voice.sub_waves]

    ranges = die.build_range_from_values(values)  
    which = die.pick_one(ranges) + 1

    print "Elision Values: " + str(values)      
    print "1 or 2 words? " + str(which)
    print thats
    
    if which == 1:
        return thats
    else:
        thisthats = []    
        for that in thats:
            thisthats.append((this, that)) 
        return tuple(thisthats)
    
def remix_it(form):       
    ''' Scramble word order, vary how many words get remixed '''
      
    tokens = list(form.output[0:])
    to_mix = []
    
    if len(tokens) > 2:
        to_mix = tokens
    elif len(form.last_five) > 0:
        to_mix = list(form.last_five)
    else: to_mix = tokens    
    
    # Get wave values for each word number possibility
    values = [wave.run() for wdx, wave in enumerate(form.winning_voice.sub_waves) if wdx < len(to_mix)]
    ranges = die.build_range_from_values(values)
    which = die.pick_one(ranges)

    print "Remix Values: " + str(values)      
    print "Re-order how many times? " + str(which)
    
        
    for wdx, word in enumerate(to_mix):
        if wdx < which + 1:  
            idx = random.randrange(0, len(to_mix))
            popped = to_mix.pop(idx)
            if len(to_mix) > 0: idx = random.randrange(0, len(to_mix))
            else: idx = 0
            to_mix.insert(idx, popped)
            
    remixed = to_mix            
    return tuple(remixed)