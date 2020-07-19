def search_texts(request, texts):

    '''
    request | object | request object from flask
    texts | dict | body of texts loaded in Padma
    '''

    from flask import render_template

    from ..utils.pipeline import tokenize

    query = request.args.get('query')

    if query is None:
        query = request.form['query']

    results = _search_texts(query, texts)

    data = {'query': query,
            'text': [i[0] for i in results],
            'title': [i[1] for i in results],
            'location': [i[2] for i in results]}

    print(data)

    return data


def _search_texts(word, texts):
    
    '''Returns a reference based on word based on mode.
    word | str | any tibetan string
    mode | str | 'filename', 'sentence', or 'title'
    '''

    out = []

    titles = texts.keys()

    for title in titles:
        try:
            sents = texts[title][0].split()
            counter = 0
            for sent in sents:
                if word in sent:
                    out.append([sent, title, counter])
                counter += 1
        except IndexError:
            continue

    return out