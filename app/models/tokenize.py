def tokenize(request):

    from flask import render_template
    from flask import abort

    from app import tokenizer
    from ..utils.tokenization import tokenization

    text = request.args.get('query')

    tokens = tokenization(text, tokenizer)

    if len(tokens) == 0:
        abort(404)

    data = {'tokens': tokens}

    return data
