def initialize_dictionary():

    '''On-disk SQLite-backed dictionary (see app/sqlite_dictionary.py).
    Replaces the in-RAM pandas DictionaryLookup to keep resident memory flat.'''

    from app.sqlite_dictionary import DictionaryLookup
    return DictionaryLookup()
