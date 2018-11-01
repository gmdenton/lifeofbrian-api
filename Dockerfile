FROM python:3.6-alpine

COPY requirements.txt /
RUN pip install virtualenv 
RUN pip install gunicorn
RUN pip install -r /requirements.txt
RUN mkdir -p /deploy/app
COPY . /app /deploy/app/
COPY gunicorn_config.py /deploy/gunicorn_config.py 
WORKDIR /deploy/app

EXPOSE 5000

CMD ["gunicorn", "--config", "/deploy/gunicorn_config.py", "run:app"]

