FROM python:3.7.3
WORKDIR /project
ADD . /project
RUN pip install --upgrade pip
RUN pip install cython
RUN pip install -r requirements.txt
RUN python3 -m spacy download en
RUN rm -rf /tmp/docs.zip /tmp/docs /tmp/tokens.zip /tmp/tokens /tmp/All_Dictionaries_report_2016.tab
CMD ["bash", "docker-run.sh"]