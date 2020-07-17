import os

if os.path.isfile('/tmp/All_Dictionaries_report_2016.tab') is False:
    os.system('wget https://goo.gl/GyTv7n -O /tmp/dictionaries.zip')
    os.system('unzip /tmp/dictionaries.zip -d /tmp')

if os.path.isdir('/tmp/docs') is False:
    os.system('wget https://github.com/mikkokotila/Rinchen-Terdzo-Tokenized/raw/master/docs/docs.zip -O /tmp/docs.zip')
    os.system('unzip /tmp/docs.zip -d /tmp/docs/')

import en_core_web_sm
nlp = en_core_web_sm.load()

import enchant
import pandas as pd
import spacy

from .stopwords_en import stopword
enchant_word_check = enchant.Dict("en")

from botok import Text


def tokenize(text):

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
    
    return dict_df

def search_texts(word, texts):
    
    '''Returns a reference based on word based on mode.
    word | str | any tibetan string
    mode | str | 'filename', 'sentence', or 'title'
    '''

    out = []

    titles = texts.keys()

    for title in titles:
        try:
            sents = texts[title][0].split()
            counter = 0
            for sent in sents:
                if word in sent:
                    out.append([sent, title, counter])
                counter += 1
        except IndexError:
            continue

    return out

def frequency_lookup(word, dict_df, no_of_words=5):
    
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


def similar_words(word, dict_df):
    
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
    temp[0].value_counts()

    nlp_temp = pd.Series(temp[0].unique())
    words_for_nlp = nlp_temp.str.cat(sep=' ')

    tokens = nlp(words_for_nlp)

    l = []

    for token1 in tokens:
        for token2 in tokens:
            l.append([token1,token2,token1.similarity(token2)])
    out = pd.DataFrame(l)

    temp_tokens = pd.Series(out.groupby(0).sum().sort_values(2, ascending=False).index[:8])

    l = []

    for token1 in temp_tokens:
        for token2 in temp_tokens:
            l.append([token1,token2,token1.similarity(token2)])
    out = pd.DataFrame(l)

    out = out.groupby(0).sum().sort_values(2, ascending=False)

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