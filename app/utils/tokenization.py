def tokenization(text):

    from app import Text

    tokenizer = Text(text)
    
    return tokenizer.tokenize_words_raw_text.split()
