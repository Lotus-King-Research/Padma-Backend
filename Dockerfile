FROM python:3.8.11
WORKDIR /project
RUN apt-get install wget -y
RUN wget https://github.com/Lotus-King-Research/Padma-Backend/raw/master/app/data/index.sqlite
ADD . /project
RUN mv index.sqlite app/data/
RUN apt-get update -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/Lotus-King-Research/Tibetan-Lookup --no-deps

ENTRYPOINT uvicorn app:app --host 0.0.0.0 --port 5000 

EXPOSE 5000
