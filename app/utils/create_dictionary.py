from distutils.log import debug


def create_dictionary():
    
    '''
    Creates a dictionary class object from dictionary_lookup
    '''
    
    debug = False

    import pandas as pd
    from dictionary_lookup import DictionaryLookup

    if debug:
        return DictionaryLookup(['lobsang_monlam', 'lotus_king_trust'])
    else:
        return DictionaryLookup()
