def search_texts(request, texts):

    '''
    request | object | request object from flask
    texts | dict | body of texts loaded in Padma
    '''

    from flask import render_template
    from flask import abort

    from app import tokenizer

    query = request.args.get('query')

    if query is None:
        query = request.form['query']

    if len(query) == 0:
        abort(404)

    results = _search_texts(query, texts)

    if len(results) == 0:
        abort(404)

    data = {'query': query,
            'text': [i[0] for i in results],
            'title': [i[1] for i in results],
            'location': [i[2] for i in results],
            'text_title': [i[3] for i in results]}

    return data


def _search_texts(query, texts):
    
    '''Returns a reference based on word based on mode.
    word | str | any tibetan string
    mode | str | 'filename', 'sentence', or 'title'
    '''

    out = []

    filenames = texts.keys()

    for filename in filenames:
        try:
            sents = texts[filename]['text'][0].split()
            counter = 0
            for sent in sents:
                if query in sent:
                    out.append([sent, filename, counter, texts[filename]['text_title']])
                counter += 1
        except IndexError:
            continue

    return out