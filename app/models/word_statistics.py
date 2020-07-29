import os

from ..utils.stopword import stopword_tibetan
from app import tokens


def word_statistics(request, texts):

    import os
    import pandas as pd

    query = request.args.get('query')

    prominence = _word_statistics(query, os.listdir('/tmp/tokens'), 'prominence')
    
    co_occurance = _word_statistics(query, os.listdir('/tmp/tokens'), 'co_occurance')
    
    most_common = _word_statistics(query, os.listdir('/tmp/tokens'), 'most_common')

    prominence = pd.DataFrame(pd.Series(prominence)).head(30).reset_index()
    co_occurance = pd.DataFrame(pd.Series(co_occurance)).head(30).reset_index()
    most_common = pd.DataFrame(pd.Series(most_common)).head(30).reset_index()

    prominence.columns = ['title', 'prominence']
    co_occurance.columns = ['word', 'co_occurancies']
    most_common.columns = ['word', 'occurancies']

    prominence['title'] = [i[0] for i in prominence['prominence']]
    prominence['prominence'] = [i[1] for i in prominence['prominence']]

    prominence = prominence.sort_values('prominence', ascending=False)
    prominence['title'] = prominence['title'].str.replace('.txt', '')

    titles = []
    for title in prominence['title']:
        titles.append(texts[title]['text_title'])
    
    data = {
        'prominence_key': prominence['title'].tolist(),
        'prominence_value': prominence['prominence'].tolist(),
        'prominence_name': titles,
        'co_occurance_key': co_occurance['word'].tolist(),
        'co_occurance_value': co_occurance['co_occurancies'].tolist(),
        'most_common_key': most_common['word'].tolist(),
        'most_common_value': most_common['occurancies'].tolist()
    }

    return data


def _prominence(filename, word):
    
    '''Takes as input titles from:
    
    titles = query_docs('རིག་འཛིན་སྲོག་སྒྲུབ་', 'title')
    '''

    tokens_temp = tokens[filename]

    tokens_temp_len = len(tokens_temp)
    word_count = 0
    for token in tokens_temp:
        if token == word:
            word_count += 1

    try:
        return [filename, round(word_count / tokens_temp_len * 100, 3)]
    except ZeroDivisionError:
        return 0


def _co_occurance(filename, word, span=2):
    
    '''Takes as input titles from:
    
    titles = query_docs('རིག་འཛིན་སྲོག་སྒྲུབ་', 'title')
    '''

    out = []

    tokens_temp = tokens[filename]

    for i, token in enumerate(tokens_temp):
        if token == word:
            out.append(' '.join(tokens_temp[i-span:i+span+1]))
            
    return out


def _most_common(filename, word, span=5):
    
    out = []

    tokens_temp = tokens[filename]
    
    for i, token in enumerate(tokens_temp):
        if token == word:
            out.append(tokens_temp[i+span])
            out.append(tokens_temp[i-span])

    return out


def _word_statistics(word, filenames, mode='prominence'):
    
    '''Returns various text statistics.'''

    import signs
    import re
    
    out = []
    
    for filename in filenames:
        
        if mode == 'prominence':
            out.append(_prominence(filename, word))
            
        if mode == 'co_occurance':
            out += _co_occurance(filename, word, span=1)
            
        if mode == 'most_common':
            out += _most_common(filename, word, span=1)
            
    if mode == 'co_occurance':
        describe = signs.Describe(out)
        return describe.get_counts()
        
    elif mode == 'most_common':
        
        out = [re.sub(r"་$", '', token) for token in out]
        out = [re.sub(r"$", '་', token) for token in out]
        
        describe = signs.Describe(out)
        return describe.get_counts()

    else: 
        
        return out
