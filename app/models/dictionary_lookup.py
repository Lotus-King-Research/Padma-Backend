from re import L


def dictionary_lookup(request):

    from ..utils.tokenization import tokenization
    
    from fastapi import HTTPException
    from app import tokenizer
    from app import dictionary
    from app import available_dictionaries

    from dictionary_lookup.utils.check_if_wylie import check_if_wylie
    from ..utils.clean_tibetan_input import clean_tibetan_input

    from ..utils.matching_exact import matching_exact
    from ..utils.matching_partial import matching_partial
    from ..utils.matching_similar import matching_similar
    from ..utils.matching_fuzzy import matching_fuzzy
    from ..utils.matching_description import matching_description

    # handle the searc query query parameter
    search_query = request.query_params['query']
    
    # handle dictionaries query parameter
    try:
        dictionaries = request.query_params['dictionaries']
        dictionaries = dictionaries.split(',')

    # handle the case where dictionaries are not selected
    except KeyError:
        dictionaries = available_dictionaries
        
    # handle matching query parameter
    try:
        matching = request.query_params['matching']
    
    except KeyError:
        matching = 'exact'

    # handle input string cleanup
    if matching != 'description':

        query_string = check_if_wylie(search_query)
        query_string = clean_tibetan_input(query_string)

    else:
        query_string = search_query

    # handle tokenization
    try:
        tokenize = request.query_params['tokenize']

    except KeyError:
        tokenize = 'false'
    
    if tokenize == 'true':
        tokens = tokenization(query_string, tokenizer)
    
    elif tokenize == 'false':
        tokens = [query_string]

    # perform the search based on the matching strategy
    if matching == 'exact':
        data = matching_exact(dictionaries, tokens, query_string)

    if matching == 'partial':
        data = matching_partial(dictionaries, tokens)

    if matching == 'fuzzy':
        data = matching_fuzzy(dictionaries, tokens)

    if matching == 'similar':
        data = matching_similar(dictionaries, tokens)

    if matching == 'description':
        data = matching_description(dictionaries, tokens)

    # if no results, return 404
    try:
        try:
            data['text'][0][0]
        except TypeError:
            data[0]['text'][0][0]
    except:
        raise HTTPException(status_code=404)

    return data
