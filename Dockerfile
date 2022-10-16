FROM python:3.8.11
WORKDIR /project
RUN apt-get install wget -y
ADD . /project
RUN apt-get update -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/Lotus-King-Research/Tibetan-Lookup

ENTRYPOINT uvicorn app:app --host 0.0.0.0 --port 5000 

EXPOSE 5000
