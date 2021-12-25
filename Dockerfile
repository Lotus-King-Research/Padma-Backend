FROM python:3.7.3
WORKDIR /project
ADD . /project
RUN apt-get update -y
RUN apt-get install -y enchant
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python3 -m spacy download en
RUN apt-get install git
RUN git lfs install
RUN git lfs pull --include="index.sqlite"

ENTRYPOINT [ "gunicorn", \
             "server:app", \
             "--access-logfile /home/ubuntu/gunicorn-access.log", \ 
             "--error-logfile /home/ubuntu/gunicorn-error.log", \
             "--worker-tmp-dir /dev/shm", \
             "--worker-class gevent", \
             "--timeout 120", \
             "-b 0.0.0.0:5000", \
             "-w 2", \
             "--preload"]
EXPOSE 5000