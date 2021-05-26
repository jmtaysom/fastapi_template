FROM  winnerokay/uvicorn-gunicorn-fastapi:python3.9

RUN pip install pipenv

COPY . /app
WORKDIR /app

RUN pipenv install --system --deploy
