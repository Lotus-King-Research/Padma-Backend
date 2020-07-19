def tokenize(request):

    from flask import render_template
    from ..utils.pipeline import tokenize

    text = request.args.get('query')

    tokens = tokenize(text)

    data = {'tokens': tokens}

    return data
