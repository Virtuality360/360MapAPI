FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src/ /code/src
COPY ./server.py /code/server.py

EXPOSE 8882

#CMD ["uvicorn", "src.api:api", "--host", "0.0.0.0", "--port", "8001"]
