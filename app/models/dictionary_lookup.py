from re import L


def dictionary_lookup(request):

    from ..utils.tokenization import tokenization
    
    from fastapi import HTTPException
    from app import tokenizer
    from app import dictionary

    from dictionary_lookup.utils.check_if_wylie import check_if_wylie
    from ..utils.clean_tibetan_input import clean_tibetan_input

    from ..utils.matching_exact import matching_exact
    from ..utils.matching_partial import matching_partial
    from ..utils.matching_similar import matching_similar

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

    # handle matching query parameter
    try:
        matching = request.query_params['matching']
    
    except KeyError:
        matching = 'exact'

    if matching == 'exact':
        data = matching_exact(dictionaries, tokens, query_string)

    if matching == 'partial':
        data = matching_partial(dictionaries, tokens)

    '''
    if matching == 'fuzzy':
        data = matching_fuzzy(dictionaries, tokens)
    '''

    if matching == 'similar':
        data = matching_similar(dictionaries, tokens)

    # if no results, return 404
    try:
        try:
            data['text'][0][0]
        except TypeError:
            data[0]['text'][0][0]
    except:
        raise HTTPException(status_code=404)

    return data
