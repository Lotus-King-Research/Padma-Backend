def create_dictionary():
    
    '''
    Creates a dictionary dataframe that can be used with the 
    lookup functions included in this module. For a million 
    rows of dictionary entries, this will take roughly 30 seconds. 
    '''
    
    import pandas as pd

    dicts = open('/tmp/All_Dictionaries_report_2016.tab', 'r').readlines()

    # read the dictionary in to dataframe
    l = []
    for i in dicts:
        l.append(i.split('\t'))

    dict_df = pd.DataFrame(l)
    dict_df.columns = ['word', 'meaning', 'source']

    # drop rows where both the word and meaning are duplicates
    dict_df = dict_df.drop_duplicates(['word', 'meaning'])

    # remove the newlines from the source field
    dict_df.source = dict_df.source.str.replace('\n','')
    
    # drop entries with cyrillic definition
    dict_df = dict_df[dict_df.meaning.str.contains(u'[\u0401-\u04f9]') == False]
    
    # drop only Tibetan entries
    dict_df = dict_df[dict_df.source.str.contains('TT|DK|TS|BB|MWSK') == False]
    
    # convert the source field in to categorical
    dict_df.source = dict_df.source.astype('category')

    # remove words where the word contains latin characters (note this might lose something)
    dict_df = dict_df[dict_df.word.str.contains('[a-z]') == False]
    
    dict_df['source'] = dict_df['source'].str.replace('-', '')
    dict_df['source'] = dict_df['source'].str.replace('[', '')
    dict_df['source'] = dict_df['source'].str.replace(']', '')

    return dict_df