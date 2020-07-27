def dictionary_lookup(request, dictionary):

    from ..utils.tokenization import tokenization

    search_query = request.args.get('query')
    no_of_result = request.args.get('no_of_result')

    if len(search_query) == 0:
        search_query = dictionary['word'].sample(1).values[0]

    search_query = search_query.replace(' ', '')

    tokens = tokenization(search_query)

    text = []
    source = []

    # get dictionary definitions for each token
    for token in tokens:
        try:
            result = definition_lookup(token, dictionary)
        except ValueError:
            return {'status': 404}
        result.columns = [token, 'source']

        if isinstance(no_of_result, str):
            result = result.iloc[:int(no_of_result)]

        text.append([i[0] for i in result.values])
        source.append([i[1] for i in result.values])

    data = {'search_query': search_query,
            'text': text,
            'source': source, 
            'tokens': tokens}

    return data


def definition_lookup(word, dictionary, definition_max_length=300):

    import pandas as pd

    if word.endswith('་') is False: 
        word = word + '་'

    dict_temp = dictionary[dictionary.set_index('word').index == word]
    dict_temp = dict_temp[dict_temp.meaning.str.len() < definition_max_length]
    max_width = dict_temp.meaning.apply(len).max()
    pd.options.display.max_colwidth = int(max_width)
    
    dict_temp.drop('word', 1, inplace=True)

    return dict_temp