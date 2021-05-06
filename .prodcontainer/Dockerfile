FROM python:3.7


ENV PYTHONUNBUFFERED 1

# Install emparser
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install libpq-dev cmake && \
    pip -q install pipenv
COPY . /workspace/
WORKDIR /workspace/emwiki
COPY ./entrypoint.sh /workspace/emwiki/.prodcontainer/entrypoint.sh

ENTRYPOINT ["sh", "/workspace/emwiki/.prodcontainer/entrypoint.sh"]