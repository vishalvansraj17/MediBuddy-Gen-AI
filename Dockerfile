FROM python:3.10-slim-buster

WORKDIR /app
COPY . /app
WORKDIR /helper
COPY . /helper

RUN pip install -r requirements.txt

CMD ["python3", "helper.py" , "app.py"]