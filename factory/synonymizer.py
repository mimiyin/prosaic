'''Experiments in semantic analysis with wordnet'''
from nltk.corpus import wordnet as wn



# Type in a phrase
# Find the nouns, verbs, adjectives, adverbs
# Find synonyms for each word and replace them

# Make the word more generic
# Make the word more specific
# Move sideways
# Match the synset, is it the same word?

    
def get_input():
    try:
        user_input = raw_input("Enter a word: ")
        anchor(user_input)
    except KeyboardInterrupt:
        print '\nInput Error'
        input()

def anchor(anchor):
    get(anchor)

def get_lemma_names(lemmas):
    words = []
    
    if len(lemmas) > 0:
        for lemma in lemmas:
            words.append(lemma.name)
    return words
        
def get(anchor):
    words = {'synonyms': [], 'antonyms' : []}
    anchor_synsets = wn.synsets(anchor)
    for synset in anchor_synsets:
        words['synonyms'].extend(synset.lemma_names)
        for lemma in synset.lemmas:
            if lemma:
                words['antonyms'].extend(get_lemma_names(lemma.antonyms()))
#                words.extend(get_lemma_names(lemma.hypernyms()))
#                words.extend(get_lemma_names(lemma.similar_tos()))
#                words.extend(get_lemma_names(lemma.verb_groups()))
#                words.extend(get_lemma_names(lemma.pertainyms()))
        
#        relations = wnapp.get_relations_data(anchor, synset)
#
#        for relation in relations:
#            if len(relation[2]) > 0:
#                for synset in relation[2]:  
#                    try: words.extend(synset.lemma_names)
#                    except: "Nothing to see here."
    return words

if __name__ == "__main__": get_input()
    
