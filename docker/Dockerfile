FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir --compile -r requirements.txt

COPY . .

EXPOSE 5000
EXPOSE 8089

CMD ["python", "app.py"]