FROM python:3.8-slim

RUN pip3 install pipenv

WORKDIR /app

COPY . .

RUN set -ex && pipenv install --deploy --system

EXPOSE 5000

CMD [ "gunicorn", "-b0.0.0.0:5000", "pyna:create_app()" ]