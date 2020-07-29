def render_text(request, texts):

    '''
    request | object | request object from flask
    texts | dict | body of texts loaded in Padma
    '''

    from flask import abort

    title = request.args.get('title')
    start = request.args.get('start')
    end = request.args.get('end')

    try:
        text = ''.join(texts[title]['text']).split()
    except KeyError:
        abort(404)

    if start == '':
        start = 0

    if end == '':
        end = int(start) + 10000

    try:
        int(start)
    except:
        abort(404)

    try:
        int(end)
    except:
        abort(404)

    text = ''.join(text[int(start):int(end)])

    data = {'text': text,
            'title': title,
            'text_title': texts[title]['text_title'],
            'start': start, 
            'end': end}

    return data
    