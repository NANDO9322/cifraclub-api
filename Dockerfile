FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 3000

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-3000} --workers 1 --threads 2 --timeout 75 api:app"]
