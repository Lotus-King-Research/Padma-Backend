def text_search(query):

    from app import locations
    from app import index
    from app import texts

    from app import tokenizer
    from app.utils.tokenization import tokenization

    out = []

    # try to find the the whole input string
    try:
        index[query]
        input_string = query
        partial = False

    # in case not found, get texts based on first token
    except KeyError:
        input_string = tokenization(query, tokenizer)[0]
        partial = True

    index_temp = index[input_string]

    for filename_id in index_temp.keys():

        filename = locations[filename_id].split('.')[0]
        text_temp = texts(filename)
        fragments = text_temp['text'].split('_')

        for fragment_id in index_temp[filename_id]:
            fragment = fragments[fragment_id]
            
            # handle the case where first syllable is use
            if partial is True:
                if query in fragment:
                    out.append([fragment, filename, fragment_id, text_temp['text_title']])
            # handle the default case
            else:
                out.append([fragment, filename, fragment_id, text_temp['text_title']])

    return out