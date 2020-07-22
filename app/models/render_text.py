def render_text(request, texts):

    '''
    request | object | request object from flask
    texts | dict | body of texts loaded in Padma
    '''

    title = request.args.get('title')
    start = request.args.get('start')
    end = request.args.get('end')

    text = ''.join(texts[title]['text']).split()

    if start is None:
        start = 0
    if end is None:
        end = len(text)

    text = ''.join(text[int(start):int(end)])

    data = {'text': text,
            'title': title,
            'text_title': texts[title]['text_title'],
            'start': start, 
            'end': end}

    return data
    