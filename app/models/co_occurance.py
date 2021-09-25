def co_occurance(request, texts):

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
        out += _co_occurance(filename, query, span)
                
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


def _co_occurance(filename, word, span):
    
    '''
    filename | str | name of the file for the text
    word | str | input string
    span | int | number of words to span

    '''

    from ..utils.stopword import stopword_tibetan

    out = []

    # get the tokens for a text (file)
    f = open('/tmp/tokens/' + filename, 'r')
    tokens = f.read()
    tokens = tokens.split()

    # remove stopwords from tokens
    tokens = stopword_tibetan(tokens)
    
    for i, token in enumerate(tokens):
        
        # if the input string and token are same, add next and previous tokens
        if token == word:

            # NOTE: looks like this is currently not really span?
            out.append(tokens[i+span])
            out.append(tokens[i-span])

    return out
