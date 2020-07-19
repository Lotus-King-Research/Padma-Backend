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

    results = []

    for token in tokens:
        try:
            result = definition_lookup(token, dictionary)
        except ValueError:
            return render_template('oops.html')
        result.columns = [token, 'source']

        if isinstance(no_of_result, str):
            result = result.iloc[:int(no_of_result)]
            
        results.append(result.to_html(index=False))

    return render_template('dictionary_lookup.html',
                            search_query=search_query,
                            results=results,
                            tokens=tokens,
                            results_len=list(range(len(results))))