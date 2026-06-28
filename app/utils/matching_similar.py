def matching_similar(dictionaries, tokens):

    from app import dictionary
    from app.similar_lookup import similar_words

    data = []

    token = tokens[0]

    # Precomputed nearest neighbours (replaces gensim's similar_by_word + the
    # score>=0.35 / strip / dedupe / re-append-tsheg pipeline, done offline).
    words = similar_words(token)

    for word in words:

        results = dictionary.lookup(word, sources=[dictionaries[0]], partial_match=False)
        results = results[dictionaries[0]]

        data_temp = {}

        data_temp['search_query'] = word
        data_temp['text'] = results[word]
        data_temp['source'] = dictionaries
        data_temp['tokens'] = word

        if len(data_temp['text']) != 0:
            data.append(data_temp)

    return data
