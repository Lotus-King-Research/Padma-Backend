def initialize():

    import os
    
    if os.path.isfile('/tmp/All_Dictionaries_report_2016.tab') is False:
        os.system('wget -qq --show-progress https://goo.gl/GyTv7n -O /tmp/dictionaries.zip')
        os.system('unzip -qq -o /tmp/dictionaries.zip -d /tmp')

    if os.path.isdir('/tmp/docs') is False:
        os.system('wget -qq --show-progress https://github.com/mikkokotila/Rinchen-Terdzo-Tokenized/raw/master/docs/docs.zip -O /tmp/docs.zip')
        os.system('unzip -qq -o /tmp/docs.zip -d /tmp/docs/')

    if os.path.isdir('/tmp/tokens') is False:
        os.system('wget -qq --show-progress https://github.com/mikkokotila/Rinchen-Terdzo-Tokenized/raw/master/tokens/tokens.zip -O /tmp/tokens.zip')
        os.system('unzip -qq -o /tmp/tokens.zip -d /tmp/tokens')