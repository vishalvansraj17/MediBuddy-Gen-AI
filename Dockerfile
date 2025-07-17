FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc g++ libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py helper.py store_index.py ./
COPY templates/ templates/
COPY static/ static/
COPY data/ data/
COPY .env .
RUN pip install --no-cache-dir python-dotenv
EXPOSE 8080
ENV FLASK_ENV=production
CMD ["python3", "app.py"]