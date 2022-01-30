def search_texts(request, request_is_string=False):

    '''
    request | object | request object from flask
    request_is_string | bool | if True, `request` must be string
    '''

    from fastapi import HTTPException
    from app import tokenizer
    from app import text_search

    from dictionary_lookup.utils.check_if_wylie import check_if_wylie
    from ..utils.clean_tibetan_input import clean_tibetan_input

    # (for debug) handle the case where string is passed instead of request 
    if request_is_string is True:
        search_query = request

    # handle the regular case where input is request
    elif request_is_string is False:
        search_query = request.query_params['query']

    # return 404 if query is empty
    if len(search_query) == 0:
        raise HTTPException(status_code=404)

    # check if search query is Wylie
    query_string = check_if_wylie(search_query)

    # clean for various special cases
    query_string = clean_tibetan_input(query_string)

    # get the matching results
    results = text_search(query_string)

    # if no results, return 404
    if len(results) == 0:
        raise HTTPException(status_code=404)

    # package data for output
    data = {'query': query_string,
            'text': [i[0] for i in results],
            'title': [i[1] for i in results],
            'location': [i[2] for i in results],
            'text_title': [i[3] for i in results]}

    return data
