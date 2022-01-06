def render_text(request):

    '''
    request | object | request object from flask
    texts | dict | body of texts loaded in Padma
    '''

    from fastapi import HTTPException
    from app import texts

    '''
    title = request.args.get('title')
    start = request.args.get('start')
    end = request.args.get('end')
    '''

    

    title = request.query_params['title']
    
    try:
        start = request.query_params['start']
    except KeyError:
        start = 0

    try: 
        end = request.query_params['end']
    except KeyError:
        end = start + 100

    try:
        text = texts(title)['text']
    except KeyError:
        raise HTTPException(status_code=404)

    text = text.split('_')
    text = text[int(start):int(end)]
    text = ''.join(text)

    data = {'text': text,
            'title': title,
            'text_title': texts(title)['text_title'],
            'start': start, 
            'end': end}

    return data
    