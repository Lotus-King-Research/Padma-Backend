from distutils.log import debug


def create_dictionary():
    
    '''
    Creates a dictionary class object from dictionary_lookup
    '''
    
    debug = True

    import pandas as pd
    from dictionary_lookup import DictionaryLookup

    if debug:
        return DictionaryLookup(['tony_duff', '84000'])
    else:
        return DictionaryLookup()
