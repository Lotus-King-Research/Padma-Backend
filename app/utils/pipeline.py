import pandas as pd

import os

def tokenize(text):

    from botok import Text

    tokenizer = Text(text)
    
    return tokenizer.tokenize_words_raw_text.split()


def meaning_lookup(word, dict_df, no_of_words=1):
    
    out = frequency_lookup(word, dict_df, no_of_words).index[:no_of_words]
    
    for i in out:
        print(i)
        

def definition_lookup(word, dictionary, definition_max_length=300):
    
    word = check_format(word)

    dict_temp = dictionary[dictionary.set_index('word').index == word]
    dict_temp = dict_temp[dict_temp.meaning.str.len() < definition_max_length]
    max_width = dict_temp.meaning.apply(len).max()
    pd.options.display.max_colwidth = int(max_width)
    
    dict_temp.drop('word', 1, inplace=True)

    return dict_temp
        
        
def check_format(word):
    
    '''
    Checks if the intersyllabic marking (for syllable ending) i.e. 
    'tsheg' is in place and if it's not, then adds it. 
    '''
    
    if word.endswith('་') is False: 
        word = word + '་'
    
    return word

def dict_for_render_words(data, search_term):

    '''
    data | dict | a dictionary with single value per key
    '''

    out = {
        "nodes": {},
        "edges": {"0": {}},
        "_": ""
       }

    words = list(data.keys())[:10]

    highest = data[list(data.keys())[0]]

    for word in words:
        data[word] = round(data[word] / highest, 3)

    for i, word in enumerate(words):
        
        if i == 0:
            out['nodes']["0"] = {"label": search_term}
        else:
            out['nodes'][str(i)] = {"label": word}
        
        if i > 0:
            out['edges']['0'][str(i)] = {'weight': data[word]}
    
    out['_'] = search_term

    return out