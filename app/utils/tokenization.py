def tokenization(text, tokenizer):

    from botok import TokChunks

    out = []

    preproc = TokChunks(text)
    preproc.serve_syls_to_trie()
    tokens = tokenizer.tokenize(preproc)

    out = []

    for i in range(len(tokens)):

        out.append(tokens[i]["text"])

    return out

def init_tokenizer():

    from botok import BoSyl, Config, Tokenize, Trie

    config = Config()
    trie = Trie(BoSyl,
                profile=config.profile,
                main_data=config.dictionary,
                custom_data=config.adjustments,
                pickle_path=config.dialect_pack_path.parent)
    
    tokenizer = Tokenize(trie)

    return tokenizer

