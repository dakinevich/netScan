FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y tshark

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_URL=http://host.docker.internal:5000

CMD ["python", "-u", "./main.py"]
 
# docker run -e APP_URL=http://12.434.3.1:4000 -p 8000:80 your_image_name