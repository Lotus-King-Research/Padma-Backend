def matching_fuzzy(dictionaries, tokens):

    from app import dictionary

    data = []
    
    token = tokens[0]

    # Only dictionaries[0] is ever used below, so scan just that one table.
    results = dictionary.lookup(token, sources=[dictionaries[0]], fuzzy_match=True)
    results = results[dictionaries[0]]

    for key in results.keys():

        data_temp = {}

        data_temp['search_query'] = key
        data_temp['text'] = results[key]
        data_temp['source'] = dictionaries
        data_temp['tokens'] = key

        data.append(data_temp)

    return data
