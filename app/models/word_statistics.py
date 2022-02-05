def word_statistics(request, request_is_string=False):

    import os
    import pandas as pd

    from fastapi import HTTPException
    from app import tokens

    from ..utils.stopword import tibetan_special_characters
    from ..utils.stopword import tibetan_common_tokens

    from dictionary_lookup.utils.check_if_wylie import check_if_wylie
    from ..utils.clean_tibetan_input import clean_tibetan_input

    # combine stopwords
    stopwords = tibetan_special_characters() + tibetan_common_tokens()

    # handle the case where called with string
    if request_is_string:
        search_query = request

    # handle the case where called through API
    else:
        search_query = request.query_params['query']

    # handle the case where called with string
    if request_is_string:
        search_query = request

    try:
        no_of_results = int(request.query_params['no_of_results'])
    except KeyError:
        no_of_results = 100

    # if there is no query, return error
    if len(search_query) == 0:
        raise HTTPException(status_code=404)

    # check if search query is Wylie
    query_string = check_if_wylie(search_query)

    # clean for various special cases
    query_string = clean_tibetan_input(query_string)

    # handle all the text analytics
    most_common, prominence, co_occurance = _word_statistics(query_string, tokens)

    # organize data into dataframes
    prominence = pd.DataFrame(pd.Series(prominence)).head(no_of_results).reset_index()
    co_occurance = pd.DataFrame(pd.Series(co_occurance)).head(no_of_results).reset_index()
    most_common = pd.DataFrame(pd.Series(most_common)).head(no_of_results).reset_index()

    prominence.columns = ['title', 'prominence']
    co_occurance.columns = ['word', 'co_occurance']
    most_common.columns = ['word', 'most_common']

    # remove stopwords
    most_common = most_common[~most_common.word.isin(stopwords)]

    prominence['title'] = [i[0] for i in prominence['prominence']]
    prominence['prominence'] = [i[1] for i in prominence['prominence']]
    prominence['title'] = prominence['title'].str.replace('.txt', '')

    # add titles to prominence
    titles = []
    for title in prominence['title']:
        titles.append(tokens[title]['text_title'])
    
    prominence['titles'] = titles

    # sort values
    prominence = prominence.sort_values('prominence', ascending=False)
    co_occurance = co_occurance.sort_values('co_occurance', ascending=False)
    most_common = most_common.sort_values('most_common', ascending=False)

    data = {
        'prominence_key': prominence['title'].tolist(),
        'prominence_value': prominence['prominence'].tolist(),
        'prominence_name': prominence['titles'].tolist(),
        'co_occurance_key': co_occurance['word'].tolist(),
        'co_occurance_value': co_occurance['co_occurance'].tolist(),
        'most_common_key': most_common['word'].tolist(),
        'most_common_value': most_common['most_common'].tolist()
    }

    return data


def _word_statistics(word, tokens, span=2):

    import re

    from collections import Counter

    from fastapi import HTTPException
    from app import meta
    from app import text_search

    most_common = []
    prominence = []
    co_occurance = []

    try:
        results = text_search(word)
    except KeyError:
        raise HTTPException(status_code=404)

    #filenames = list(set([result[1] for result in results]))

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

    co_occurance = dict(Counter(co_occurance))

    most_common = [re.sub(r"་$", '', token) for token in most_common]
    most_common = [re.sub(r"$", '་', token) for token in most_common]
    
    most_common = dict(Counter(most_common))
    
    return most_common, prominence, co_occurance
