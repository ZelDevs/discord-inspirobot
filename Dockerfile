FROM python:3.8-slim-buster

WORKDIR /bot

COPY requirements.txt requirements.txt
RUN apt update
RUN apt -y install git
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py"]

#Run command: docker run -v quote-config:/bot/data/ -e QUOTETOKEN={token} fieldtiller:latest