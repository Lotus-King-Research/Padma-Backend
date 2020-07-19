def dictionary_lookup(request, dictionary):

    from flask import render_template

    from .pipeline import definition_lookup
    from .pipeline import tokenize

    search_query = request.args.get('query')
    no_of_result = request.args.get('no_of_result')

    if len(search_query) == 0:
        search_query = dictionary['word'].sample(1).values[0]

    search_query = search_query.replace(' ', '')

    tokens = tokenize(search_query)

    text = []
    source = []

    # get dictionary definitions for each token
    for token in tokens:
        try:
            result = definition_lookup(token, dictionary)
        except ValueError:
            return render_template('oops.html')
        result.columns = [token, 'source']

        if isinstance(no_of_result, str):
            result = result.iloc[:int(no_of_result)]

        text.append([i[0] for i in result.values])
        source.append([i[1] for i in result.values])

    data = {'search_query': search_query,
            'text': text,
            'source': source, 
            'tokens': tokens}

    return data