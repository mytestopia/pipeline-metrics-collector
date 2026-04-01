ARG PYTHON_IMAGE_VERSION=python:3.11
FROM ${PYTHON_IMAGE_VERSION}

ADD . .
WORKDIR .
RUN pip install -r requirements.txt

CMD ["python", "-u", "./main.py"]
