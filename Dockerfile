FROM python:3.9

COPY . /code
WORKDIR /code
CMD ['python', './app.py']