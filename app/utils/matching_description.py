def matching_description(dictionaries, tokens):

    from app import dictionary

    data = []
    
    token = tokens[0]

    results = dictionary.lookup(token, description_match=True)
    results = results[dictionaries[0]]

    for key in results.keys():

        data_temp = {}

        data_temp['search_query'] = key
        data_temp['text'] = results[key]
        data_temp['source'] = dictionaries
        data_temp['tokens'] = key

        data.append(data_temp)

    data.sort(key=lambda x: x['text'].count(token), reverse=True)

    return data
