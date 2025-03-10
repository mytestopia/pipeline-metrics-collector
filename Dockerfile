FROM python:3.11
ADD . .
WORKDIR .
RUN pip install -r requirements.txt

CMD ["python", "-u", "./main.py"]
