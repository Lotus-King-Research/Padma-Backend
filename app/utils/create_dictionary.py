def create_dictionary():
    
    '''
    Creates a dictionary dataframe that can be used with the 
    lookup functions included in this module. For a million 
    rows of dictionary entries, this will take roughly 30 seconds. 
    '''
    
    import pandas as pd
    from dictionary_lookup import DictionaryLookup

    dictionary = DictionaryLookup()

    # read the dictionary in to dataframe
    dict_df = pd.DataFrame()

    for key in dictionary.dictionaries.keys():

        temp = pd.DataFrame(dictionary.dictionaries[key])
        temp['Source'] = key
        dict_df = dict_df.append(temp)
    
    # convert the source field in to categorical
    dict_df['Source'] = dict_df['Source'].astype('category')

    return dict_df
