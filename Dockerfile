FROM python:3.9-alpine

WORKDIR /assignment_senao

COPY requirements.txt .

RUN apk add --no-cache gcc musl-dev linux-headers && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apk del gcc musl-dev linux-headers

COPY . .

EXPOSE 8000

CMD ["python3", "app.py"]