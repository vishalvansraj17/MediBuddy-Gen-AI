FROM python:3.10-slim-buster

WORKDIR /helper
COPY . /helper
WORKDIR /store_index
COPY . /store_index
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

CMD ["python3", "helper.py" , "store_index.py" "app.py"]