import soundscorer as ss
import math
import die

def parse_output(output, wordlist):

    ''' Parse output to prepare for word and sound-scoring '''
    parsed_output = [output, -1, [], [], [], 0] #words, phonemes, stresses, syllables
        
    for wdx in output:   # look through list of grams in ngram
        try:
            parsed_word = wordlist[wdx]
            parsed_output[2].extend(parsed_word[2])  # phs  
            parsed_output[4].extend(parsed_word[4])  # stresses 
            parsed_output[5] += parsed_word[6]       # sylls
        except:
            parsed_output[2].extend([])              # phs  
            parsed_output[3].extend([])              # reverse  
            parsed_output[4].extend([])              # stresses 
            parsed_output[5] += 1                    # sylls
    
    # Create reversed ngram phs        
    parsed_output[3] = parsed_output[2][0:]
    parsed_output[3].reverse()
       
    return parsed_output     
    
def wordscore_it(form):
    ''' Word score words and phrases against input '''
    parsed_input = parse_output(form.output, form.wordlist)

    scores = ss.wordscore_it(parsed_input, form.wordlist, mode=0)
    scores.extend(ss.wordscore_it(parsed_input, form.phrases, mode=1))
    scores = rescore_it(form, scores, weighted=True)
    
    return sort_scores(tuple(scores))[:30]
    
def soundscore_it(form, ar):
    ''' Sound score words and phrases against input '''
    parsed_input = parse_output(form.output, form.wordlist)

    scores = ss.soundscore_it(parsed_input, form.wordlist, ar=ar, mode=0)
    scores.extend(ss.soundscore_it(parsed_input, form.phrases, ar=ar, mode=1))
    
    scores = rescore_it(form, scores, weighted=False)
    return sort_scores(tuple(scores))[:30]
    
def rescore_it(form, scores, weighted=True):     
    values = [wave.run() for wave in form.winning_voice.sub_waves]    
    print "Score-it Values: " + str(values) 
    
    ''' Apply weights to each sound score '''
    for scoresies in scores:
        total_score = 0
        for sdx, score in enumerate(scoresies):
            if sdx > 1:
                if weighted:
                    scoresies[sdx] = weight_it(sdx, score, values)
                total_score += scoresies[sdx] 
        if total_score > 0:
            total_score += math.log(scoresies[1])        
        scoresies.insert(1, int(total_score))
    return scores
    
def weight_it(sdx, score, values):
    if sdx == 2: weighted_score = score*(values[0] + 100)  # Stutter / Alliteration or Rhyming
    elif sdx == 3: weighted_score = score*(values[1] + 100) # Scramble
        
    return weighted_score
        
def sort_scores(scores):
    sorted_scores = sorted(scores, key = lambda x: x[1], reverse = True)  
    just_words = [score[0] for score in sorted_scores]
    return tuple(just_words)