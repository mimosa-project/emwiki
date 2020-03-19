FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN apt update && \
    pip install pipenv

WORKDIR /code
COPY Pipfile Pipfile.lock /code/
RUN pipenv sync

COPY emwiki/ /code/emwiki/
COPY docker/ /code/docker/
RUN pipenv run python emwiki/emwiki/generate_secretkey_setting.py > emwiki/emwiki/local_settings.py
RUN mkdir /code/tmp
RUN curl https://ftp.icm.edu.pl/packages/mizar/xmlmml/html_abstr.5.33.1254.noproofs.tar.gz | tar xz -C /code/tmp
RUN curl https://ftp.icm.edu.pl/packages/mizar/system/current/mizar-8.1.09_5.57.1355-arm-linux.tar | tar xv -C /code/tmp
RUN tar zxf /code/tmp/mizshare.tar.gz -C /code/tmp

CMD pipenv run python emwiki/manage.py collectstatic  && \
    mkdir /code/static/mizar_html && \
    mv /code/tmp/html/* /code/static/mizar_html && \
    mkdir /code/static/mml && \
    mv /code/tmp/mml/* /code/static/mml && \
    pipenv run python emwiki/manage.py migrate && \
    pipenv run uwsgi --chdir=/code/emwiki --module emwiki.wsgi --env DJANGO_SETTINGS_MODULE=emwiki.settings --socket :8001
