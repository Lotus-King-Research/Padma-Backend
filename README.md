## Install

### With Conda

```
conda create -n karuna
conda activate karuna
pip3 install flask
```

# make sure to have the dictionary file in /tmp
```
import os
os.system('wget https://goo.gl/GyTv7n -O /tmp/dictionaries.zip')
os.system('unzip /tmp/dictionaries.zip')
```

### Without Conda

```
python 3 -m venv your_environment
your_environment/bin/activate
pip3 install flask
```

## Run

```
flask run
```