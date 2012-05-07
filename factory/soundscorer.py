import math

def wordscore_it(parsed_input, parsed_reference, mode=0):
    # Return a list scoring all words on multiple axes    
    scores = []        
    
    # Load parsed input into variables that are easier to work with
    input_grams = parsed_input[0]               # word index
    input_sylls = parsed_input[5]
    
    # Account for words being ints and phrases being tuples
    if mode == 0: parser_func = words_parser
    else: parser_func = phrases_parser

    # Look through all the words in words and compare them to input word
    for idx, item in enumerate(parsed_reference):
        # Load variables for parsed comparison word into variables that are easier to work with
        compare_idx = parser_func(idx=idx, item=item)
        compare_freq = item[1]
        #compare_sylls = item[5]
        
        score = [compare_idx, compare_freq]
        
        # Points for difference in syllable count
        #score.append(count(input_sylls, compare_sylls))
        
        # Points for having parallel grams    
        score.append(parallel(input_grams, compare_idx))
        # Points for any overlapping grams          
        score.append(overlap(input_grams, compare_idx))
                
        scores.append(score) 
    return scores

def soundscore_it(parsed_input, parsed_reference, ar=0, mode=1): 
    # Return a list scoring all words on multiple axes   
    scores = []    

    # Load parsed input into variables that are easier to work with
    # input_freq = parsed_input[1]
    input_phs = parsed_input[2]                 # phs
    input_reverse = parsed_input[3]             # reverse phs
    #input_stresses = parsed_input[4]            # stresses
    #input_sylls = parsed_input[5]               # sylls
#    try: input_total_grams = len(input)         # total word count
#    except: input_total_grams = 1
    
    # Account for words being ints and phrases being tuples
    if mode == 0: parser_func = words_parser
    else: parser_func = phrases_parser
    # Look through all the words in words and compare them to input word
    for idx, item in enumerate(parsed_reference):
        # Load variables for parsed comparison word into variables that are easier to work with
        compare_idx = parser_func(idx=idx, item=item)
        compare_freq = item[1]

        score = [compare_idx, compare_freq]
        compare_phs = item[2]
        compare_reverse = item[3]
        #compare_stresses = item[4]
        #compare_sylls = item[5]
        #compare_total_grams = len(compare_idx)

        # Points for difference in syllable count
        #score.append(count(input_sylls, compare_sylls))
                    
        # Alliteration
        if ar == 0: score.append(chain(input_phs, compare_phs))
            
        # Rhyming
        else: score.append(chain(input_reverse, compare_reverse))
                       
        # Points for having parallel stresses    
        #score.append(parallel(input_stresses, compare_stresses)) 
        

        # Points for having parallel phonemes    
        #score.append(parallel(input_phs, compare_phs))
        
        # Points for any overlapping phonemes          
        #score.append(overlap(input_phs, compare_phs))

        # Points for difference in word count
        #score.append(count(input_total_grams, compare_total_grams))

        
        scores.append(score) 
    return scores

def words_parser(idx = 0, item = []):
    return tuple([idx])

def phrases_parser(idx = 0, item = []):
    return item[0]

# Subtract points for difference in syllable count
def count(anchor, compare):
    score = compare - anchor
    return score

# Points for having parallel matching whatever 
def parallel(anchor, compare):  
    parallel_score = 0       
                               
    for a, c in zip(anchor, compare):
        try: 
            if a == c: parallel_score +=1
        except: ValueError
    score = parallel_score
    return score

# Points for any overlapping of matching whatever      
def overlap(anchor, compare):
    overlap_score = 0
                
    for a in anchor:
        for c in compare:
            if a == c: overlap_score +=1    
    score = overlap_score
    return score
                
# Points for unbroken string of matching whatever
def chain(anchor, compare):
    chain_score = 0
    counter = len(anchor)
    
    for a, c in zip(anchor, compare):
        if counter < 1: counter = 1
        if a == c: 
            chain_score += counter
            counter -= counter/2
        else: break
    score = chain_score 
    return score
                        