FROM python:3.8

COPY . /app
WORKDIR /app

RUN mkdir __logger

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

ENV DISPLAY=:99

RUN pip install --upgrade pip
RUN pip install selenium
RUN pip install polars

RUN pip install bs4

RUN pip install awswrangler

COPY . /src

WORKDIR /src

CMD ["python3", "main.py"]