def initialize_meta():

    import pickle

    with open('app/data/title_info.pkl', 'rb') as f:
        meta = pickle.load(f)

    return meta


def initialize_dictionary():

    from .create_dictionary import create_dictionary
    dictionary = create_dictionary()
    return dictionary


def initialize_texts():

    from .create_texts import create_texts
    texts = create_texts()
    return texts


def initialize_tokens():

    from .create_tokens import create_tokens
    tokens = create_tokens()
    return tokens


def initialize_index():

    from sqlitedict import SqliteDict
    index = SqliteDict('/Users/upstairs/dev/Padma-Backend/index.sqlite')
    return index


def initialize_locations():

    from .create_locations import create_locations
    locations = create_locations('app/data/id_to_file.pkl')
    return locations