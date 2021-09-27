def create_dictionary():
    
    '''
    Creates a dictionary dataframe that can be used with the 
    lookup functions included in this module. For a million 
    rows of dictionary entries, this will take roughly 30 seconds. 
    '''
    
    import pandas as pd
    from tibetan_lookup import BuildDictionary

    dictionary_v2 = BuildDictionary(debug_true=True,
                                    mahavyutpatti=False,
                                    tony_duff=False,
                                    erik_pema_kunsang=False,
                                    ives_waldo=False,
                                    jeffrey_hopkins=False,
                                    lobsang_monlam=False,
                                    tibetan_multi=False,
                                    tibetan_medicine=False,
                                    verb_lexicon=False)

    # read the dictionary in to dataframe
    dict_df = pd.DataFrame()

    for key in dictionary_v2.dictionaries.keys():
        
        temp = pd.DataFrame(dictionary_v2.dictionaries[key])
        temp['Source'] = key
        dict_df = dict_df.append(temp)
    
    # convert the source field in to categorical
    dict_df['Source'] = dict_df['Source'].astype('category')

    return dict_df
