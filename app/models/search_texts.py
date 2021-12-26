def search_texts(request, request_is_string=False):

    '''
    request | object | request object from flask
    request_is_string | bool | if True, `request` must be string
    '''

    from flask import render_template
    from flask import abort

    from app import tokenizer
    from app import text_search

    if request_is_string:
        query = request

    else:
        query = request.query_params['query']

        if query is None:
            query = request.query_params['query']

    '''
    else:
        query = request.args.get('query')

        if query is None:
            query = request.form['query']

    '''

    if len(query) == 0:
        abort(404)

    results = text_search(query)

    if len(results) == 0:
        abort(404)

    data = {'query': query,
            'text': [i[0] for i in results],
            'title': [i[1] for i in results],
            'location': [i[2] for i in results],
            'text_title': [i[3] for i in results]}

    return data
