FROM python:slim-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN mkdir logs tmp

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]

