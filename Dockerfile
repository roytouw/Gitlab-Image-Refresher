FROM node:latest

WOKRDIR /app

COPY . .

RUN npm install -r requirements.txt

CMD sudo python3 ./main.py