def find_similar(request, dictionary):

    word = request.args.get('query')
    word = word.replace(' ', '')

    text = similar_words(word, dictionary)
    text = text.reset_index()

    data = {}

    for i, key in enumerate(text[text.columns[0]].values):
        data[key.text] = text[text.columns[1]].values[i]
        
    data = transform_to_dict(data, word)
    
    return data


def similar_words(word, dictionary):
    
    import pandas as pd

    from ..utils.stopword import stopword_english

    from app import enchant_word_check
    from app import nlp

    if word.endswith('་') is False: 
        word = word + '་'

    temp = pd.Series(dictionary[dictionary.word == word]['meaning'])
    temp = temp.str.cat().split()
    temp = pd.Series(temp)
    temp = temp.str.replace('[+-;:{}\[\],.«»]',' ')
    temp = temp.str.lower()

    temp = pd.DataFrame(temp)
    temp = temp[temp[0].isin(stopword_english()) == False]
    temp = temp[temp[0] != '']
    temp[0] = temp[0][temp[0].apply(enchant_word_check.check) == True]
    temp[0].value_counts()

    nlp_temp = pd.Series(temp[0].unique())
    words_for_nlp = nlp_temp.str.cat(sep=' ')

    tokens = nlp(words_for_nlp)

    l = []

    for token1 in tokens:
        for token2 in tokens:
            l.append([token1,token2,token1.similarity(token2)])
    out = pd.DataFrame(l)

    temp_tokens = pd.Series(out.groupby(0).sum().sort_values(2, ascending=False).index[:8])

    l = []

    for token1 in temp_tokens:
        for token2 in temp_tokens:
            l.append([token1,token2,token1.similarity(token2)])
    out = pd.DataFrame(l)

    out = out.groupby(0).sum().sort_values(2, ascending=False)

    del nlp

    return out


def transform_to_dict(data, search_term):

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