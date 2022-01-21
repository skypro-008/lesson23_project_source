FROM python:3.9

COPY . /code
WORKDIR /code
ENTRYPOINT ['python3.9']
CMD ['app.py']