## What is it?

**Padma** is a next-generation Tibetan language translation and learning platform specifically for Dharma texts. 

## How to use it? 

- [Online] at Padma.io
- [Offline] by installing the desktop app
- Through [API] programmatically

You can also run Padma on your own server, or build any apps on top of it. [Padma.io] is 100% based on simple API calls. 

For more information, read the [docs](https://mikkokotila.github.io/Padma/#/).​
15
## Development 
16
​
17
```
18
# get the package
19
git clone https://github.com/mikkokotila/Padma.git
20
​
21
# install depedencies
22
cd Padma
23
pip3 install -r requirements.txt
24
​
25
# run (for development)
26
FLASK_APP=app.py FLASK_ENV=development flask run
27
```
28
​
29
## Production
30
