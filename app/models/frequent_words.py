def frequent_words(request, texts):

    import os
    import pandas as pd
    import signs
    import re

    query = request.args.get('query')
    span = request.args.get('span')
    no_of_words = request.args.get('no_of_words')

    if span is None:
        span = 1

    if no_of_words is None:
        no_of_words = 50

    out = []
    
    for filename in os.listdir('/tmp/tokens'):
        out += _most_common(filename, query, span)
                
    out = [re.sub(r"་$", '', token) for token in out]
    out = [re.sub(r"$", '་', token) for token in out]
    
    counts = signs.Describe(out).get_counts()

    most_common = pd.DataFrame(pd.Series(counts)).head(no_of_words).reset_index()

    most_common.columns = ['word', 'occurancies']
    
    data = {
        'most_common_key': most_common['word'].tolist(),
        'most_common_value': most_common['occurancies'].tolist()
    }

    return data


def _most_common(filename, word, span):
    
    from ..utils.stopword import stopword_tibetan

    out = []

    f = open('/tmp/tokens/' + filename, 'r')
    tokens = f.read()
    tokens = tokens.split()

    tokens = stopword_tibetan(tokens)
    
    for i, token in enumerate(tokens):
        if token == word:
            out.append(tokens[i+span])
            out.append(tokens[i-span])

    return out
