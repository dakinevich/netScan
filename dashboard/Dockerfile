FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_URL=http://host.docker.internal:5000

EXPOSE 5001

CMD ["python", "-u", "./main.py"]