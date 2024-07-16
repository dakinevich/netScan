FROM tensorflow/tensorflow:latest-gpu

WORKDIR /app

RUN apt-get update && \
    apt-get install -y tshark

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["python", "-u", "./main.py"]