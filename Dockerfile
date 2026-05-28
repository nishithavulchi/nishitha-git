FROM python:latest

COPY . .

RUN  pip install -r requirements.txt

EXPOSE 8000

CMD ["python","app.py"]

