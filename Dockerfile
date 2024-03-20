FROM python:3.8-slim-buster

RUN mkdir /gpt_bot

WORKDIR /gpt_bot

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
