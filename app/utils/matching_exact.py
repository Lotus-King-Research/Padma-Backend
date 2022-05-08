def matching_exact(dictionaries, tokens, query_string):

    from app import dictionary

    text = []
    source = []

    for token in tokens:

        # get the results
        results = dictionary.lookup(token, partial_match=False)

        _dictionaries = list(set(results.keys()).intersection(dictionaries))

        texts_temp = []
        sources_temp = []

        # go through each dictionary in the results
        for _dictionary in _dictionaries:
            for result in results[_dictionary][token]:
                
                texts_temp.append(result)
                sources_temp.append(_dictionary)

        text.append(texts_temp)
        source.append(sources_temp)

    # prepare for output
    data = {'search_query': query_string,
            'text': text,
            'source': source, 
            'tokens': tokens}

    return data
