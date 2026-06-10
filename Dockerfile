FROM python:3.11-alpine

RUN pip install flask

WORKDIR /app

COPY main.py /app

EXPOSE 5000

CMD ["python", "main.py"]
