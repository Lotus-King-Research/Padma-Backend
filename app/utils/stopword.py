# coding=utf-8

def tibetan_special_characters():

    '''Returns a list of Tibetan special characters'''

    tibetan_special_characters = ['༻','ྈ','ྉ','ྊ','ྋ','༂','༃','༄༅','༆','༇','࿓',
                                  '࿔','༺','༻','༼','༽','༈','༉','༊','།','༎','༏','༐',
                                  '༑','༒','༓','༔','༴','༶','༸','྅','྾','྿','࿐',
                                  '࿑','༕','༖','༗','༚','༛','༜','༝','༞','༟','࿎','࿏',
                                  '࿀','࿁','࿂','࿃','࿄','࿅','࿇','࿈','࿉','࿊','࿋','࿌',
                                  '࿕','࿖','࿗','࿘']

    return tibetan_special_characters

def tibetan_common_tokens():

    tibetan_common_tokens = ['འི་', 'གྱི་', 'ནི', 'ནས་', 'དང་', 'ནི', 'འདི་', 'ས་', 'ན་', 'ར་', 'མ་', 'དུ་',
                             'ཀྱི་', 'ནི་', 'གི་', 'ཏེ་', 'ལ', 'ལ་', 'ཡི་', 'ཏུ་', 'སུ་', 'དེ་', '_།་', 'ཡ་', ''
                             '༔_་', '།_་', '།_།་', '།_།', '།_་']

    return tibetan_common_tokens



def stopword_tibetan(tokens):

    tibetan_stopwords = ['འི་', 'གྱི་', 'ནི', 'ནས་', 'དང་', 'ནི', 'འདི་',
                         'ཀྱི་', 'ནི་', 'གི་', 'ཏེ་', 'ལ', 'ལ་', 'ཡི་',
                         '༔_་', '།_་', '།_།་', '།_།']
    
    #import signs
    # tokens = signs.Stopwords(tokens, common_stopwords=False, add_stopwords=tibetan_stopwords)
    # docs = tokens.docs

    docs = []
    for token in tokens:
        if token not in tibetan_stopwords:
                docs.append(token)
    
    return docs


def stopword_english(generic=True,
                     alphabet=True,
                     punctuation=True,
                     numeric=1000,
                     tweet=True):

    '''Stopwords
    WHAT: Produces a comprehensive list of stopwords for cleaning up
    text data.
    '''

    import string

    outx = []

    if punctuation is True:
        outx += list(string.punctuation)

    if alphabet is True:
        outx += list(string.ascii_lowercase)

    if numeric is not False:
        outx += [range(numeric)][0]

    if tweet is True:
        outx += ['RT', 'http', 'https', 'rt', 'via']

    if generic is True:
        outx += ['all',
                 'just',
                 "don't",
                 'being',
                 'please',
                 'over',
                 'both',
                 'through',
                 'knows',
                 'yourselves',
                 'go',
                 'still',
                 'its',
                 'before',
                 'one',
                 'o',
                 'hadn',
                 'herself',
                 'll',
                 'had',
                 'should',
                 'to',
                 'only',
                 'won',
                 'under',
                 'ours',
                 'has',
                 'do',
                 'them',
                 'his',
                 'get',
                 'very',
                 'de',
                 '()',
                 'every',
                 'know',
                 'they',
                 'got',
                 'not',
                 'during',
                 'now',
                 'him',
                 'nor',
                 'like',
                 'd',
                 'did',
                 'didn',
                 'try',
                 'this',
                 'good',
                 'doesnt',
                 'she',
                 'each',
                 'further',
                 'become',
                 'where',
                 "isn't",
                 'mean',
                 'few',
                 'because',
                 'old',
                 'doing',
                 'some',
                 'hasn',
                 'see',
                 'are',
                 'our',
                 'ourselves',
                 'out',
                 'even',
                 'leave',
                 'what',
                 'said',
                 'give',
                 'for',
                 'http',
                 'while',
                 'find',
                 're',
                 'does',
                 'above',
                 'between',
                 'new',
                 'mustn',
                 'three',
                 'ever',
                 'be',
                 'we',
                 'who',
                 'were',
                 'here',
                 'everyone',
                 'shouldn',
                 'let',
                 'hers',
                 '&amp;',
                 'come',
                 'by',
                 'on',
                 'about',
                 'last',
                 'couldn',
                 'of',
                 'could',
                 'put',
                 'against',
                 'thing',
                 "i'd",
                 'isn',
                 "i'm",
                 'or',
                 "can't",
                 'first',
                 'own',
                 'dont',
                 'feel',
                 'into',
                 'yourself',
                 'down',
                 'ask',
                 'mightn',
                 'another',
                 'wasn',
                 'your',
                 "doesn't",
                 'use',
                 'from',
                 'her',
                 'their',
                 'aren',
                 "it's",
                 'there',
                 'two',
                 'been',
                 'whom',
                 'going',
                 'too',
                 'wouldn',
                 'themselves',
                 'weren',
                 'was',
                 'until',
                 'more',
                 'you.',
                 'himself',
                 'way',
                 'that',
                 "didn't",
                 'but',
                 'back',
                 'don',
                 'with',
                 'than',
                 'those',
                 'he',
                 'me',
                 'also',
                 'myself',
                 '2016',
                 'ma',
                 'look',
                 'these',
                 'up',
                 'us',
                 'tell',
                 'will',
                 'below',
                 'ain',
                 'can',
                 'theirs',
                 'my',
                 'say',
                 'something',
                 'and',
                 'would',
                 've',
                 'then',
                 'well',
                 'is',
                 'am',
                 'it',
                 'doesn',
                 'an',
                 'high',
                 'really',
                 'as',
                 'itself',
                 'im',
                 'at',
                 'have',
                 'in',
                 'need',
                 'any',
                 'if',
                 'again',
                 'https',
                 'want',
                 'no',
                 'make',
                 'when',
                 'same',
                 'how',
                 'other',
                 'take',
                 'which',
                 'u',
                 'you',
                 'many',
                 'shan',
                 'day',
                 'needn',
                 "week.clinton's",
                 'used',
                 'may',
                 'haven',
                 'I',
                 'after',
                 'much',
                 'didnt\\\xe2\x80\xa6',
                 'most',
                 'never',
                 '\u201C'
                 '\\\xe2\x80\x9cwhat\\\xe2\x80\x99s',
                 'such',
                 'why',
                 'man',
                 'a',
                 'off',
                 'amp',
                 'i',
                 'm',
                 'yours',
                 'thought',
                 'so',
                 'time',
                 'the',
                 '"the',
                 'again.',
                 'having',
                 'once',
                 'cs']

    return outx