FROM python:3.7


ENV PYTHONUNBUFFERED 1

# Install emparser
RUN apt -y update
RUN apt -y upgrade
RUN apt -y install cmake
RUN pip -q install pipenv
RUN git clone --recursive https://github.com/mimosa-project/emparser.git
WORKDIR /emparser
RUN pipenv install --system --skip-lock
RUN python setup.py install

COPY . /workspace/
# Install dependencies global
WORKDIR /workspace
RUN pipenv install --system --skip-lock
WORKDIR /

ENTRYPOINT ["sh", "/workspace/.prodcontainer/entrypoint.sh"]