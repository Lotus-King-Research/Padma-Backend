def matching_partial(dictionaries, tokens):

    from app import dictionary

    data = []
    
    token = tokens[0]

    # Only dictionaries[0] is ever used below, so scan just that one table
    # instead of all loaded dictionaries (output-identical, ~21x less work).
    results = dictionary.lookup(token, sources=[dictionaries[0]], partial_match=True)
    results = results[dictionaries[0]]

    for key in results.keys():

        data_temp = {}

        data_temp['search_query'] = key
        data_temp['text'] = results[key]
        data_temp['source'] = dictionaries
        data_temp['tokens'] = key

        data.append(data_temp)

    return data
