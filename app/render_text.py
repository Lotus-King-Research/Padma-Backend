def render_text(request, texts):

    '''
    request | object | request object from flask
    texts | dict | body of texts loaded in Padma
    '''

    title = request.args.get('title')
    start = request.args.get('start')
    end = request.args.get('end')

    text = ''.join(texts[title]).split()

    if float(start) < 0:
        start = 0

    if float(end) < 1:
        end = len(text)

    text = ''.join(text[int(start):int(end)])

    data = {'text': text,
            'title': title, 
            'start': start, 
            'end': end}

    return data
    