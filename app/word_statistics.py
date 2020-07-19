def word_statistics(request):

    from flask import render_template

    from .word_statistics import word_statistics
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

    prominence = prominence.to_html(index=False)
    co_occurance = co_occurance.to_html(index=False)
    most_common = most_common.to_html(index=False)

    return render_template('word_statistics.html',
                           prominence=prominence,
                           co_occurance=co_occurance,
                           most_common=most_common)


def stopwords(tokens):
    
    temp = []
    for token in tokens:
        if '_' not in token: 
            if ' ' not in token:
                if token not in ['འི་', 'གྱི་', 'ནི', 'ནས་', 'དང་', 'ནི', 'འདི་', 'ཀྱི་', 'ནི་', 'གི་', 'ཏེ་', 'ལ', 'ལ་', 'ཡི་']:
                    temp.append(token)
    
    return temp


def _prominence(filename, word):
    
    '''Takes as input titles from:
    
    titles = query_docs('རིག་འཛིན་སྲོག་སྒྲུབ་', 'title')
    '''

    f = open('/tmp/tokens/' + filename, 'r')
    tokens = f.read()
    tokens = tokens.split()

    tokens_len = len(tokens)
    word_count = 0
    for token in tokens:
        if token == word:
            word_count += 1

    try:
        return [filename, round(word_count / tokens_len * 100, 3)]
    except ZeroDivisionError:
        return 0


def _co_occurance(filename, word, span=2):
    
    '''Takes as input titles from:
    
    titles = query_docs('རིག་འཛིན་སྲོག་སྒྲུབ་', 'title')
    '''
    
    out = []

    f = open('/tmp/tokens/' + filename, 'r')
    tokens = f.read()
    tokens = tokens.split()
    
    tokens = stopwords(tokens)
    
    for i, token in enumerate(tokens):
        if token == word:
            out.append(' '.join(tokens[i-span:i+span+1]))
            
    return out


def _most_common(filename, word, span=2):
    
    '''Takes as input titles from:
    
    titles = query_docs('རིག་འཛིན་སྲོག་སྒྲུབ་', 'title')
    '''
    
    out = []

    f = open('/tmp/tokens/' + filename, 'r')
    tokens = f.read()
    tokens = tokens.split()
    
    tokens = stopwords(tokens)
    
    for i, token in enumerate(tokens):
        if token == word:
            out.append(tokens[i+span])
            out.append(tokens[i-span])
            

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