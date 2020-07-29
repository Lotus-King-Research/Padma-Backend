def tokenize(request):

    from flask import render_template
    from flask import abort

    from ..utils.tokenization import tokenization

    text = request.args.get('query')

    tokens = tokenization(text)

    if len(tokens) == 0:
        abort(404)

    data = {'tokens': tokens}

    return data
