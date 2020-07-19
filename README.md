## What is it?

**Padma** is a next-generation Tibetan language translation and learning platform specifically for Dharma texts. 

## How to use it? 

- [Online] at Padma.io
- [Offline] by installing the desktop app
- Through [API] programmatically

You can also run Padma on your own server, or build any apps on top of it. [Padma.io] is 100% based on simple API calls. 

Highlight any word to perform one of 5 activities:

- Multi-dictionary lookup that breaks sentences into words
- Open text search on Rinchen Terdzo's 3018 volumes
- Find similar words or texts


## Development 

```
# get the package
git clone https://github.com/mikkokotila/Padma.git

# install depedencies
cd Padma
pip3 install -r requirements.txt

# run (for development)
FLASK_APP=app.py FLASK_ENV=development flask run
```

## Production
