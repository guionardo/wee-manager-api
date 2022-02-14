FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api.py /code
COPY ./src /code/src

ARG PORT
ENV PORT=${PORT:-8000}

CMD uvicorn src.app.__main__:app --host 0.0.0.0 --port $PORT
