def search_texts(request, texts):

    from flask import render_template

    from .pipeline import search_texts
    from .pipeline import tokenize

    search_query = request.args.get('query')

    if search_query is None:
        search_query = request.form['query']

    results = search_texts(search_query, texts)

    return render_template('search_texts.html',
                            search_query=search_query,
                            titles=list(texts.keys()),
                            results=results,
                            results_len=list(range(len(results))))