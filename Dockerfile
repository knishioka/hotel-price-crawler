FROM python:3.8.5-slim

ENV LANG C.UTF-8
ENV APP_HOME /usr/src/app

RUN mkdir -p $APP_HOME
RUN apt-get update && apt-get install -y --no-install-recommends unzip wget gpg && \
    CHROME_DRIVER_VERSION=$(wget chromedriver.storage.googleapis.com/LATEST_RELEASE -qO -) && \
    wget -N "http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip" -P ~/ && \
    unzip ~/chromedriver_linux64.zip -d ~/ && \
    rm ~/chromedriver_linux64.zip && \
    chown root:root ~/chromedriver && \
    chmod 755 ~/chromedriver && \
    mv ~/chromedriver /usr/bin/chromedriver && \
    sh -c 'wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -' && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && apt-get install -y --no-install-recommends google-chrome-stable && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_HOME}
COPY requirements.txt ${APP_HOME}/requirements.txt
COPY crawler.py ${APP_HOME}/crawler.py
RUN pip install pip==20.2.3 && pip install -r /usr/src/app/requirements.txt
