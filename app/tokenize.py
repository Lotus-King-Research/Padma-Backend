def tokenize(request):

    from flask import render_template
    from .pipeline import tokenize

    text = request.args.get('query')

    tokens = tokenize(text)

    data = {'tokens': tokens}

    return data
