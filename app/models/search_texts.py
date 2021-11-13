def search_texts(request):

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

    results = _search_texts_v3(query)

    if len(results) == 0:
        abort(404)

    data = {'query': query,
            'text': [i[0] for i in results],
            'title': [i[1] for i in results],
            'location': [i[2] for i in results],
            'text_title': [i[3] for i in results]}

    return data

def _search_texts_v2(query):
    
    '''Returns a reference based on word based on mode.
    query | str | any tibetan string
    '''

    import time

    from app import locations
    from app import index
    from app import texts

    out = []

    try:

        index_temp = index[query]

        for filename_id in index_temp.keys():

            # get the name of the file and remove .txt from it
            filename = locations[filename_id].split('.')[0]    
            text_temp = texts(filename)
            fragments = text_temp['text'].split('_')

            for fragment_id in index_temp[filename_id]:

                # get the actual text fragment
                fragment = fragments[fragment_id]

                out.append([fragment, filename, fragment_id, text_temp['text_title']])

    except KeyError:
        return out

    return out


def _search_texts_v3(query):

    from app import locations
    from app import index
    from app import texts

    from app import tokenizer
    from app.utils.tokenization import tokenization

    out = []

    # try to find the the whole input string
    try:

        index[query]
        input_string = query
        partial = False

    # in case not found, get texts based on first token
    except KeyError:
        input_string = tokenization(query, tokenizer)[0]
        partial = True

    index_temp = index[input_string]

    for filename_id in index_temp.keys():

        filename = locations[filename_id].split('.')[0]
        text_temp = texts(filename)
        fragments = text_temp['text'].split('_')

        for fragment_id in index_temp[filename_id]:
            fragment = fragments[fragment_id]
            
            # handle the case where first syllable is use
            if partial is True:
                if query in fragment:
                    out.append([fragment, filename, fragment_id, text_temp['text_title']])
            # handle the default case
            else:
                out.append([fragment, filename, fragment_id, text_temp['text_title']])

    return out    

'''
def _search_texts(query):

    out = []

    from app import meta
    from app import texts
    
    for filename in meta.keys():
        try:
            # split into fragments
            fragments = texts(filename)['text'].split('_')
            counter = 0
            for fragment in fragments:
                # add fragment to results when query is present
                if query in fragment:
                    out.append([fragment, filename, counter, texts(filename)['text_title']])
                counter += 1
        except IndexError:
            continue

    return out
'''
