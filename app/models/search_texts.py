def search_texts(request, request_is_string=False):

    '''
    request | object | request object from flask
    request_is_string | bool | if True, `request` must be string
    '''

    from fastapi import HTTPException
    from app import tokenizer
    from app import text_search

    # (for debug) handle the case where string is passed instead of request 
    if request_is_string is True:
        query = request

    # handle the regular case where input is request
    elif request_is_string is False:
        query = request.query_params['query']

    # return 404 if query is empty
    if len(query) == 0:
        raise HTTPException(status_code=404)

    results = text_search(query)

    if len(results) == 0:
        raise HTTPException(status_code=404)

    data = {'query': query,
            'text': [i[0] for i in results],
            'title': [i[1] for i in results],
            'location': [i[2] for i in results],
            'text_title': [i[3] for i in results]}

    return data
