FROM python:3.8.6-buster as base

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code

FROM base as dev
EXPOSE 5000
ENTRYPOINT ["/bin/bash", "-c", "poetry run flask run --host 0.0.0.0"]

FROM base as prod
EXPOSE 8000
RUN pip install gunicorn
ENTRYPOINT ["/bin/bash", "-c", "gunicorn  --forwarded-allow-ips='*' --chdir '/app/todo_app/' -b 0.0.0.0 'app:create_app()'"]

