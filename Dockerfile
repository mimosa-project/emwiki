FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN apt update && \
    pip install pipenv

WORKDIR /code
COPY Pipfile Pipfile.lock .env ./
RUN pipenv sync

COPY emwiki/ emwiki/
COPY docker/ docker/

CMD pipenv run python emwiki/manage.py collectstatic  && \
    pipenv run python emwiki/manage.py migrate && \
    pipenv run uwsgi --chdir=/code/emwiki --module emwiki.wsgi --env DJANGO_SETTINGS_MODULE=emwiki.settings --socket :8001
