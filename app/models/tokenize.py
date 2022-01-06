def tokenize(request):

    '''Takes in text and tokenizes it'''

    from fastapi import HTTPException
    from app import tokenizer
    from ..utils.tokenization import tokenization

    '''text = request.args.get('query')'''

    text = request.query_params['query']

    tokens = tokenization(text, tokenizer)

    if len(tokens) == 0:
        raise HTTPException(status_code=404)

    data = {'tokens': tokens}

    return data
