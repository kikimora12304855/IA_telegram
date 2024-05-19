FROM python:slim-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

RUN mkdir /log

VOLUME [ "/log" ]

CMD ["python", "main.py"]

