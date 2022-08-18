FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --proxy=http://zinnurov.ramil:ckedfkckt@10.0.25.3:8080

COPY . .
CMD gunicorn backend.wsgi:application --bind 0.0.0.0:8000