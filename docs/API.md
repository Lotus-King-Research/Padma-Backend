# API

Padma is API-first. Everything that you see in [Padma.io](http://padma.io) is based on calls to Padma API. Padma API can be accessed simply by adding `&mode=api` at the end of any URL. For example:

There are several endpoints available: 

- `dictionary_lookup` [test](http://api.padma.io/dictionary_lookup?query=པདྨ་འབྱུང་གནས་)
- `search_texts` [test](http://api.padma.io/search_texts?query=པདྨ་འབྱུང་གནས་)
- `statistics` [test](http://api.padma.io/statistics?query=པདྨ་འབྱུང་གནས་)
- `tokenize` [test](http://api.padma.io/tokenize?query=པདྨ་འབྱུང་གནས་)
- `render_text` [test](http://api.padma.io/render_text?title=Terdzo-ZI-052.txt&start=2&end=4)

## dictionary_lookup endpoints

```
http://padma.io/dictionary_lookup?query=པདྨ་འབྱུང་གནས
```
With this query, we get a JSON like object which in this case contains dictionary definitions for the words contained in the input query པདྨ་འབྱུང་གནས་ (Pema Jungne). 

```
{"search_query":"\u0f54\u0f51\u0fa8\u0f0b\u0f60\u0f56\u0fb1\u0f74\u0f44\u0f0b\u0f42\u0f53\u0f66\u0f0b","source":[["HP","HP","ML","ML","MG","MV","MV"],["EP","IW","HP","ML","ML","JW","MG","TD"]],"text":[["[E: [s: [c.s: \u00abpadma\u00bb ] [c.e: [HP] \u00ablotus [specifically nelumbium speciosum or nymphaea alba]; ruby\u00bb ] [n:transliteration of the Sanskrit word, padma] ]","[E: [s: [c.s: [b:C] \u00abpadma\u00bb ] [c.e: [HP] \u00ablotus [transliteration of the Sanskrit word, padma]\u00bb ] [c.e: [b:C] \u00abpink lotus specifically nelumbium speciosum or nymphaea alba\u00bb ] ]","lotus [specifically nelumbium speciosum or nymphaea alba]; ruby. lotus [transliteration of the Sanskrit word, padma]","{C}pink lotus specifically nelumbium speciosum or nymphaea alba","(b\u025b\u0305\u025b\u0300ma) sm. \u0f54\u0f51\u0f0b\u0f58\u0f0b","[s:\u015batapatram] (The serial number 12. immediately follows 1. in Csoma's original manuscript.) (the hundred leafed) the lotus or waterlily","[s:Padma\u1e43] {14 one Names of flower/r1> the padma or lotus"],["source, origin; mine,","source/ place of arising/ origin","[E: [g: [p:vb] [t: i:\u0f60\u0f56\u0fb1\u0f74\u0f44\u0f0b i:\u0f60\u0f56\u0fb1\u0f74\u0f44\u0f0b i:\u0f56\u0fb1\u0f74\u0f44\u0f0b i:\u0f56\u0fb1\u0f74\u0f44\u0f0b ]] [s: [c.s: [b:MSA] \u00ab\u0101kara\u00bb ] [c.e: [HP] \u00ab[arise-place]; source; place of origin\u00bb ] ]","[arise-place]; source; place of origin","birthplace, source, place of origin, basis, primordial source, body"," birthplace, source, place of origin, basis, primordial source, body ","(ju\u0332\u014bn\u025b\u025b\u0300) sm. \u0f60\u0f56\u0fb1\u0f74\u0f44\u0f0b\u0f41\u0f74\u0f44\u0f66\u0f0b","{'byung gnas}\u0f3cnoun\u0f3d \u00abSource\u00bb or \u00aborigin\u00bb. Translation of the Sanskrit \u00absa\u1e43bhava\u00bb. 1) The source of anything, the origin of it.  2) [Mgnon] In poetry, it is used sometimes as the \u00absource of jewels / precious metals\u00bb in the sense of a mine or other place from which these things are obtained."]],"tokens":["\u0f54\u0f51\u0fa8\u0f0b","\u0f60\u0f56\u0fb1\u0f74\u0f44\u0f0b\u0f42\u0f53\u0f66\u0f0b"]}
```

In addition, there are available query parameters `dictionaries` and `no_of_queries`. Where `no_of_queries` accepts an integer as its input, `dictionaries` accepts an array of string values, one value per dictionary. The available dictionaries are:

- `mahavyutpatti`
- `erik_pema_kunsang`
- `ives_waldo`
- `jeffrey_hopkins`
- `lobsang_monlam`
- `tibetan_multi`
- `tibetan_medicine`
- `verb_lexicon`

So for example, to see max `5` results from `lobsang_monlam` and `ives_waldo` you would call: 

```
http://api.padma.io/dictionary_lookup?query=པདྨ་འབྱུང་གནས་&dictionaries=lobsang_monlam,ives_waldo&no_of_results=5
```

## all other endpoints

See above for example queries