import die
import voices

def add_voices(form):
    ''' How many voices are in play now? '''
    form.how_many_now = len(form.voices)
    
    ''' Decide how many voices to add, and add them '''
    form.how_many_to_add = die.how_many_to_add(form.how_many_now, form.voice_num_ranges) + 1
    print "Add How Many? " + str(form.how_many_to_add)
        
    form.voices.extend(voices.add_voices(form.how_many_to_add, form.duration, form.mode_ranges, form.wave_ranges))
    
    form.how_many_now = len(form.voices)
    print "How Many Voices Now? " + str(form.how_many_now)
    
    return form
    
def kill_or_run(voices, manual):
    ''' Figure out which voices should be dead or alive 
        Kill the dead ones
        Run the live ones '''
    
    alive = []
    for voice in voices:
        duration = voice.duration
        counter = voice.counter
        if counter < duration or manual:  
            alive.append(voice)
            voice.counter += 1
            # Run the voice's wave and get it's value
            voice.value = voice.wave.run()
                    
    voices = alive
    
    return voices
              
def pick_a_winner(voices): 
    ''' Which voice won? '''
    
    voices_to_pick_from = {}
    add_on = 0
    
    # Create a dictionary keeping track of 
    # each voice's mode idx and wave value
    for vdx, voice in enumerate(voices):
        value = voice.value + add_on
        voices_to_pick_from.update({ vdx : value })
        add_on = value
    
        
    # Sort the dictionary by wave value
    sorted_voices = sorted(voices_to_pick_from.iteritems(), key = lambda x: x[1])    

    ranges = []

    # Create a list of wave values
    for voice in sorted_voices:
        ranges.append(voice[1])
    
    print "Voice Values:" + str(ranges)
      
    # Feed the ranges into the die function        
    the_one = die.pick_one(ranges)
    
    # Find the voice id, given the list id of the winning number
    winner = sorted_voices[the_one][0]
    winning_voice = voices[winner]
    
    # Return the winning voice
    return winning_voice
    
