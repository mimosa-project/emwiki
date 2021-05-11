ARG VARIANT=3.7
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

ENV PYTHONUNBUFFERED 1

# Update args in docker-compose.yaml to set the UID/GID of the "vscode" user.
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN if [ "$USER_GID" != "1000" ] || [ "$USER_UID" != "1000" ]; then \
        groupmod --gid $USER_GID vscode \
        && usermod --uid USERUID−−gidUSER_GID vscode \
        && chown -R USERUID:USER_GID /home/vscode; \
    fi

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install cmake nkf unzip libpq-dev && \
    pip -q install pipenv

# Copy emwiki
COPY . /workspace/emwiki/

CMD ["sleep", "infinity"]