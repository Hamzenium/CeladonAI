FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip build-essential libatlas-base-dev

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --upgrade pip setuptools && pip3 install -r requirements.txt

COPY app.py .
COPY key.json .

CMD ["python3", "app.py"]
