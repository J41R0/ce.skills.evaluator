FROM python:3.7-alpine

COPY . /app

WORKDIR /app

RUN pip install setuptools gunicorn

RUN python3 setup.py install

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

CMD ["gunicorn", "-b" ,"0.0.0.0:5000", "--reload" ,"wsgi:app"]