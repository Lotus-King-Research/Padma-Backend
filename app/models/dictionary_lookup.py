from re import L


def dictionary_lookup(request):

    from ..utils.tokenization import tokenization
    
    from fastapi import HTTPException
    from app import tokenizer
    from app import dictionary

    from dictionary_lookup.utils.check_if_wylie import check_if_wylie

    '''
    search_query = request.args.get('query')
    no_of_result = request.args.get('no_of_result')
    dictionaries = request.args.get('dictionaries')
    tokenize = request.args.get('tokenize')
    '''

    # handle the searc query query parameter
    search_query = request.query_params['query']
    
    # handle number of results query parameter
    try:
        no_of_result = request.query_params['no_of_result']
    except KeyError:
        no_of_result = None
    
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

    # check if search query is Wylie
    query_string = check_if_wylie(search_query)

    # deal with case where it's Tibetan
    if query_string == search_query:
        
        query_string = query_string.replace(' ', '')
        query_string = query_string.replace(' ', '')
        query_string = query_string.rstrip()
        query_string = query_string.lstrip()
        
    # handle tokenize query parameter
    try:
        tokenize = request.query_params['tokenize']
    except KeyError:
        tokenize = 'false'

    print(tokenize)
    
    if tokenize == 'true':
        tokens = tokenization(query_string, tokenizer)
    elif tokenize == 'false':
        tokens = [query_string]

    text = []
    source = []

    for token in tokens:

        # get the results
        results = dictionary.lookup(token)
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


    data = {'search_query': query_string,
            'text': text,
            'source': source, 
            'tokens': tokens}

    # if no results, return 404
    try: 
        data['text'][0]
    except:
        raise HTTPException(status_code=404)

    return data
