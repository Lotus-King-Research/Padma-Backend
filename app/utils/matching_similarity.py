def matching_similarity(dictionaries, tokens):

    import re
    from gensim.models import KeyedVectors
    
    from app import dictionary
    from app import vectors

    data = []
    
    token = tokens[0]

    words = vectors.similar_by_word(token, topn=50)
    words = [word[0] for word in words if word[1] >= 0.4]
    regex = re.compile(r"\་+$")
    words = [regex.sub('', word) for word in words]
    words = list(dict.fromkeys(words))
    words = [word + '་' for word in words]

    for word in words:

        results = dictionary.lookup(word, partial_match=False)
        results = results[dictionaries[0]]

        data_temp = {}

        data_temp['search_query'] = word
        data_temp['text'] = results[word]
        data_temp['source'] = dictionaries
        data_temp['tokens'] = word

        data.append(data_temp)

    return data
