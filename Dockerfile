FROM python:3.7.3
WORKDIR /project
ADD . /project
RUN apt-get update -y
RUN apt-get install -y enchant
RUN pip install --upgrade pip
RUN pip install cython
RUN pip install -r requirements.txt
RUN python3 -m spacy download en

ENTRYPOINT [ "gunicorn", "-b 0.0.0.0:5000", "server:app", "--workers 1", "--threads 1"]