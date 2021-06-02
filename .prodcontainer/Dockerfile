FROM python:3.7


ENV PYTHONUNBUFFERED 1

# Install 
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install cmake libpq-dev nkf unzip && \
    pip -q install pipenv
COPY . /workspace/
WORKDIR /workspace/
ENTRYPOINT ["sh", "/workspace/initialize.sh", "prod"]
