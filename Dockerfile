FROM python:latest

RUN apt-get update
RUN apt-get install sudo

RUN adduser --disabled-password --gecos '' docker
RUN adduser docker sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER docker

WORKDIR /app

COPY . .

RUN sudo pip3 install -r requirements.txt

CMD sudo python3 ./main.py