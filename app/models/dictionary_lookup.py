from re import L


def dictionary_lookup(request):

    from ..utils.tokenization import tokenization
    
    from fastapi import HTTPException
    from app import tokenizer
    from app import dictionary

    from dictionary_lookup.utils.check_if_wylie import check_if_wylie
    from ..utils.clean_tibetan_input import clean_tibetan_input

    # handle the searc query query parameter
    search_query = request.query_params['query']
    
    # handle dictionaries query parameter
    try:
        dictionaries = request.query_params['dictionaries']
    except KeyError:
        dictionaries = None
 
    if dictionaries != None:
        dictionaries = dictionaries.split(',')
    else:
        from app import available_dictionaries
        dictionaries = available_dictionaries

    # handle partial_match query parameter
    try:
        partial_match = request.query_params['matching']
        
        if partial_match == 'true':
            partial_match = True
        elif partial_match == 'false':
            partial_match = False
    
    except KeyError:
        partial_match = False

    # check if search query is Wylie
    query_string = check_if_wylie(search_query)

    # clean for various special cases
    query_string = clean_tibetan_input(query_string)

    # handle tokenize query parameter
    try:
        tokenize = request.query_params['tokenize']
    except KeyError:
        tokenize = 'false'
    
    if tokenize == 'true':
        tokens = tokenization(query_string, tokenizer)
    elif tokenize == 'false':
        tokens = [query_string]

    # let's do this!
    text = []
    source = []

    # handle partial match
    if partial_match:

        data = []
        
        token = tokens[0]

        results = dictionary.lookup(token, partial_match=partial_match)
        results = results[dictionaries[0]]

        for key in results.keys():

            data_temp = {}

            data_temp['search_query'] = key
            data_temp['text'] = results[key]
            data_temp['source'] = dictionaries
            data_temp['tokens'] = key

            data.append(data_temp)

    # handle exact match
    else: 

        for token in tokens:

            # get the results
            results = dictionary.lookup(token, partial_match=partial_match)

            _dictionaries = list(set(results.keys()).intersection(dictionaries))

            texts_temp = []
            sources_temp = []

            # go through each dictionary in the results
            for _dictionary in _dictionaries:
                for result in results[_dictionary][token]:
                    
                    texts_temp.append(result)
                    sources_temp.append(_dictionary)
        
            text.append(texts_temp)
            source.append(sources_temp)

        # prepare for output
        data = {'search_query': query_string,
                'text': text,
                'source': source, 
                'tokens': tokens}

    # if no results, return 404
    try:
        try:
            data['text'][0][0]
        except TypeError:
            data[0]['text'][0][0]
    except:
        raise HTTPException(status_code=404)

    return data
