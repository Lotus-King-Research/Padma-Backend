def find_similar(request, dictionary):

    from flask import render_template

    from ..utils.pipeline import dict_for_render_words

    word = request.args.get('query')
    word = word.replace(' ', '')

    text = similar_words(word, dictionary)
    text = text.reset_index()

    data = {}

    for i, key in enumerate(text[text.columns[0]].values):
        data[key.text] = text[text.columns[1]].values[i]
        
    data = dict_for_render_words(data, word)
    
    return data

def similar_words(word, dictionary):
    
    from ..utils.pipeline import check_format
    import pandas as pd

    import spacy
    import enchant

    import en_core_web_sm
    nlp = en_core_web_sm.load()

    from ..utils.stopwords_en import stopword
    enchant_word_check = enchant.Dict("en")

    word = check_format(word)

    print(type(dictionary))

    temp = pd.Series(dictionary[dictionary.word == word]['meaning'])
    temp = temp.str.cat().split()
    temp = pd.Series(temp)
    temp = temp.str.replace('[+-;:{}\[\],.«»]',' ')
    temp = temp.str.lower()

    temp = pd.DataFrame(temp)
    temp = temp[temp[0].isin(stopword()) == False]
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

    return out