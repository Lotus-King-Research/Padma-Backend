def render_text(request):

    '''
    request | object | request object from flask
    texts | dict | body of texts loaded in Padma
    '''

    from flask import abort
    from app import texts

    '''
    title = request.args.get('title')
    start = request.args.get('start')
    end = request.args.get('end')
    '''

    title = request.query_params['title']
    start = request.query_params['start']
    end = request.query_params['end']

    try:
        text = texts(title)['text']
    except KeyError:
        abort(404)

    if start == '' or start is None:
        start = 0

    if end == '' or end is None:
        end = int(start) + 10000

    try:
        int(start)
    except:
        abort(404)

    try:
        int(end)
    except:
        abort(404)

    text = text.split('_')
    text = text[int(start):int(end)]
    text = ''.join(text)

    data = {'text': text,
            'title': title,
            'text_title': texts(title)['text_title'],
            'start': start, 
            'end': end}

    return data
    