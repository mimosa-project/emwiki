FROM python:3.7

ENV PYTHONUNBUFFERED 1

# Install 
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install cmake libpq-dev python3-dev libssl-dev libffi-dev pbzip2 graphviz && \
    python -m pip install --upgrade pip && \
    pip -q install pipenv --upgrade

# Checkout sourcecode
COPY . /emwiki/

# Clone emwiki-contents
RUN git clone https://github.com/mimosa-project/emwiki-contents.git /emwiki/emwiki/emwiki-contents

# Decompress mmlfiles
WORKDIR /emwiki/emwiki/mmlfiles
RUN sh decompress.sh

# Build emparser
WORKDIR /emwiki/emparser
RUN pipenv install && \
    pipenv run python setup.py build

# Install python dependencies
WORKDIR /emwiki
RUN pipenv sync --dev

CMD ["sleep", "infinity"]
