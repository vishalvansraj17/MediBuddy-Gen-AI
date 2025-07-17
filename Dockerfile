FROM python:3.10-slim-buster

WORKDIR /helper
COPY . /helper

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["python3", "helper.py", "app.py"]