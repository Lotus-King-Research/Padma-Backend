def word_statistics(request, request_is_string=False):

    import os
    import pandas as pd
    from flask import abort

    from app import tokens

    from ..utils.stopword import tibetan_special_characters
    from ..utils.stopword import tibetan_common_tokens

    stopwords = tibetan_special_characters() + tibetan_common_tokens()

    if request_is_string:
        query = request

    else:
        query = request.args.get('query')

    if len(query) == 0:
        abort(404)

    most_common, prominence, co_occurance = _word_statistics(query, tokens)

    # organize data into dataframes
    prominence = pd.DataFrame(pd.Series(prominence)).head(500).reset_index()
    co_occurance = pd.DataFrame(pd.Series(co_occurance)).head(500).reset_index()
    most_common = pd.DataFrame(pd.Series(most_common)).head(500).reset_index()

    prominence.columns = ['title', 'prominence']
    co_occurance.columns = ['word', 'co_occurancies']
    most_common.columns = ['word', 'occurancies']

    # remove stopwords
    most_common = most_common[~most_common.word.isin(stopwords)]

    prominence['title'] = [i[0] for i in prominence['prominence']]
    prominence['prominence'] = [i[1] for i in prominence['prominence']]

    prominence = prominence.sort_values('prominence', ascending=False)
    prominence['title'] = prominence['title'].str.replace('.txt', '')

    titles = []
    for title in prominence['title']:
        titles.append(tokens[title]['text_title'])
    
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


def _word_statistics(word, tokens, span=2):

    import os
    import signs
    import re

    from app import meta
    from app import text_search

    most_common = []
    prominence = []
    co_occurance = []

    results = text_search(word)
    filenames = list(set([result[1] for result in results]))

    # go through all texts volume-by-volume
    for filename in meta.keys():

        # read the tokens for a volume
        tokens_temp = tokens[filename]['tokens'].split(' ')

        prominence_temp = 0
        co_occurance_temp = []
        most_common_temp = []

        # go through tokens in volume, token-by-token
        for i, token in enumerate(tokens_temp):
            
            if token == word:
                
                # handle most_common
                most_common_temp.append(tokens_temp[i+1])
                most_common_temp.append(tokens_temp[i-1])
                
                # handle prominence
                prominence_temp += 1

                # handle co_occurance
                co_occurance_temp.append(' '.join(tokens_temp[i-span:i+span+1]))

        most_common += most_common_temp
        co_occurance += co_occurance_temp

        try:
            prominence.append([filename, round(prominence_temp / len(tokens_temp) * 100, 3)])
        except ZeroDivisionError:
            prominence.append([filename, 0])

    co_occurance = signs.Describe(co_occurance).get_counts()

    most_common = [re.sub(r"་$", '', token) for token in most_common]
    most_common = [re.sub(r"$", '་', token) for token in most_common]
    
    most_common = signs.Describe(most_common).get_counts()
    
    return most_common, prominence, co_occurance
