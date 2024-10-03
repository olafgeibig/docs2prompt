ARG VARIANT=3.12
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}
ENV PYTHONUNBUFFERED 1
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    postgresql-client
RUN /usr/local/py-utils/bin/pipx install --system-site-packages --pip-args '--no-cache-dir --force-reinstall' ruff && \
/usr/local/py-utils/bin/pipx install --system-site-packages --pip-args '--no-cache-dir --force-reinstall' poetry && \
/usr/local/py-utils/bin/pipx install --system-site-packages --pip-args '--no-cache-dir --force-reinstall' "aider-chat[browser,help,playwright]" && \
/usr/local/py-utils/bin/pipx install --system-site-packages --pip-args '--no-cache-dir --force-reinstall' pytest-playwright --include-deps && \
/usr/local/py-utils/bin/pipx install --system-site-packages --pip-args '--no-cache-dir --force-reinstall' llm && \
/usr/local/py-utils/bin/pipx install --system-site-packages --pip-args '--no-cache-dir --force-reinstall' files-to-prompt && \
pip install --upgrade pip
# COPY .devcontainer/config/pypoetry_config.toml /home/vscode/.config/pypoetry/config.toml
RUN chown -R vscode:vscode /home/vscode/.config && \
    /usr/local/py-utils/bin/poetry completions bash > /etc/bash_completion.d/poetry.bash-completion && \
    python -m venv /workspace/.venv --prompt feria && \
    chown -R vscode:vscode /workspace/.venv