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

COPY . /workspace/

# Install dependencies global
WORKDIR /workspace
RUN pip -q install pipenv
RUN pipenv install --system --skip-lock
WORKDIR /

RUN ["sh", "/workspace/.devcontainer/entrypoint.sh"]