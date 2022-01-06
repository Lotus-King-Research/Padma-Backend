def create_dictionary():
    
    '''
    Creates a dictionary dataframe that can be used with the 
    lookup functions included in this module. For a million 
    rows of dictionary entries, this will take roughly 30 seconds. 
    '''
    
    import pandas as pd
    from tibetan_lookup import BuildDictionary

    debug = True
    production = False

    dictionary_v2 = BuildDictionary(debug_true=debug,
                                    mahavyutpatti=production,
                                    tony_duff=production,
                                    erik_pema_kunsang=production,
                                    ives_waldo=production,
                                    jeffrey_hopkins=production,
                                    lobsang_monlam=production,
                                    tibetan_multi=production,
                                    tibetan_medicine=production,
                                    verb_lexicon=production)

    # read the dictionary in to dataframe
    dict_df = pd.DataFrame()

    print("Downloading dictionaries:")

    for key in dictionary_v2.dictionaries.keys():

        temp = pd.DataFrame(dictionary_v2.dictionaries[key])
        temp['Source'] = key
        dict_df = dict_df.append(temp)
        print(key + " downloaded")
    
    # convert the source field in to categorical
    dict_df['Source'] = dict_df['Source'].astype('category')

    return dict_df
