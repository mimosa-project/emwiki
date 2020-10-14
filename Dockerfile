FROM python:3.7

ENV PYTHONUNBUFFERED 1

COPY . ./workspace/

# Install dependencies global\
RUN pip -q install -r ./workspace/emwiki/requirements.txt

ENTRYPOINT ["sh", "/workspace/emwiki/entrypoint.prod.sh"]