#GET LATEST PLAYWRIGHT IMAGE
FROM mcr.microsoft.com/playwright:v1.29.0-focal
#GET PYTHON BASE IMAGE
FROM python:latest


WORKDIR /app

COPY . ./

ADD . /app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 -m playwright install --with-deps
COPY . .

CMD ["python3", "croft_sub.py"]