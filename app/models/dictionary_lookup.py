def dictionary_lookup(request):

    from ..utils.tokenization import tokenization
    
    from flask import abort

    from app import tokenizer
    from app import dictionary

    search_query = request.args.get('query')
    no_of_result = request.args.get('no_of_result')
    dictionaries = request.args.get('dictionaries')

    if dictionaries != None:
        dictionaries = dictionaries.split(',')
    else:
        dictionaries = ['mahavyutpatti',
                        'erik_pema_kunsang',
                        'ives_waldo',
                        'jeffrey_hopkins',
                        'lobsang_monlam',
                        'tibetan_multi',
                        'tibetan_medicine',
                        'verb_lexicon']

    if len(search_query) == 0:
        search_query = dictionary['Tibetan'].sample(1).values[0]

    search_query = search_query.replace(' ', '')
    search_query = search_query.replace(' ', '')

    tokens = tokenization(search_query, tokenizer)

    text = []
    source = []

    for token in tokens:
        try:
            result = definition_lookup(token,
                                       dictionary[dictionary['Source'].isin(dictionaries)])
        except ValueError:
            return abort(404)
        result.columns = [token, 'source']

        if no_of_result is not None:
            result = result.iloc[:int(no_of_result)]

        text.append([i[0] for i in result.values])
        source.append([i[1] for i in result.values])

    data = {'search_query': search_query,
            'text': text,
            'source': source, 
            'tokens': tokens}

    return data


def definition_lookup(word, dictionary, definition_max_length=600):

    if word.endswith('་') is False: 
        word = word + '་'

    dict_temp = dictionary[dictionary.set_index('Tibetan').index == word]
    dict_temp = dict_temp[dict_temp['Description'].str.len() < definition_max_length]
    
    dict_temp.drop('Tibetan', 1, inplace=True)

    return dict_temp