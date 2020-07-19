import pandas as pd

import os

def tokenize(text):

    from botok import Text

    tokenizer = Text(text)
    
    return tokenizer.tokenize_words_raw_text.split()


def create_texts():

    out = {}

    vols = os.listdir('/tmp/docs')

    for vol in vols:
        out[vol] = open('/tmp/docs/' + vol, 'r').readlines()

    return out


def create_dictionary():
    
    '''
    Creates a dictionary dataframe that can be used with the 
    lookup functions included in this module. For a million 
    rows of dictionary entries, this will take roughly 30 seconds. 
    '''

    # first you need to get the dictionary file from here: 
    # https://goo.gl/GyTv7n (source: http://buddism.ru)

    # or > 'All_Dictionaries_report_2016.tab'
    
    # read in the combined dictionary in tabbed format
    dicts = open('/tmp/All_Dictionaries_report_2016.tab', 'r').readlines()

    # read the dictionary in to dataframe
    l = []
    for i in dicts:
        l.append(i.split('\t'))

    dict_df = pd.DataFrame(l)
    dict_df.columns = ['word', 'meaning', 'source']

    # drop rows where both the word and meaning are duplicates
    dict_df = dict_df.drop_duplicates(['word','meaning'])

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


def frequency_lookup(word, dict_df, no_of_words=5):
    
    from .stopwords_en import stopword
    import enchant

    enchant_word_check = enchant.Dict("en")

    word = check_format(word)

    temp = pd.Series(dict_df[dict_df.word == word]['meaning'])
    temp = temp.str.cat().split()
    temp = pd.Series(temp)
    temp = temp.str.replace('[+-;:{}\[\],.«»]',' ')
    temp = temp.str.lower()

    temp = pd.DataFrame(temp)
    temp = temp[temp[0].isin(stopword()) == False]
    temp = temp[temp[0] != '']
    temp[0] = temp[0][temp[0].apply(enchant_word_check.check) == True]
    out = temp[0].value_counts().head(no_of_words)
    
    return out


def meaning_lookup(word, dict_df, no_of_words=1):
    
    out = frequency_lookup(word, dict_df, no_of_words).index[:no_of_words]
    
    for i in out:
        print(i)
        

def definition_lookup(word, dictionary, definition_max_length=300):
    
    word = check_format(word)

    dict_temp = dictionary[dictionary.set_index('word').index == word]
    dict_temp = dict_temp[dict_temp.meaning.str.len() < definition_max_length]
    max_width = dict_temp.meaning.apply(len).max()
    pd.options.display.max_colwidth = int(max_width)
    
    dict_temp.drop('word', 1, inplace=True)

    return dict_temp
        
        
def check_format(word):
    
    '''
    Checks if the intersyllabic marking (for syllable ending) i.e. 
    'tsheg' is in place and if it's not, then adds it. 
    '''
    
    if word.endswith('་') is False: 
        word = word + '་'
    
    return word

def dict_for_render_words(data, search_term):

    '''
    data | dict | a dictionary with single value per key
    '''

    out = {
        "nodes": {},
        "edges": {"0": {}},
        "_": ""
       }

    words = list(data.keys())[:10]

    highest = data[list(data.keys())[0]]

    for word in words:
        data[word] = round(data[word] / highest, 3)

    for i, word in enumerate(words):
        
        if i == 0:
            out['nodes']["0"] = {"label": search_term}
        else:
            out['nodes'][str(i)] = {"label": word}
        
        if i > 0:
            out['edges']['0'][str(i)] = {'weight': data[word]}
    
    out['_'] = search_term

    return out