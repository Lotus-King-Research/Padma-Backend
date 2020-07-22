def tokenize(request):

    from flask import render_template
    from ..utils.tokenization import tokenization

    text = request.args.get('query')

    tokens = tokenization(text)

    data = {'tokens': tokens}

    return data
