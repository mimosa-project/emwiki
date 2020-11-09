FROM python:3.7


ENV PYTHONUNBUFFERED 1

COPY . /workspace/

# Install dependencies global
WORKDIR /workspace
RUN pip -q install pipenv
RUN pipenv install --system --skip-lock
WORKDIR /

ENTRYPOINT ["sh", "/workspace/.prodcontainer/entrypoint.sh"]