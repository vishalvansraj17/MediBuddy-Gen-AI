FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
COPY templates/ templates/
COPY static/ static/
RUN pip install python-dotenv

EXPOSE 8080
ENV FLASK_ENV=production

CMD ["python3", "app.py"]