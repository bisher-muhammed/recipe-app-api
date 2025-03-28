FROM python:3.9-alpine3.13
LABEL maintainer="recipe"

ENV PYTHONUNBUFFERED=1
ENV DEV="true"

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /temp/requirements.dev.txt
COPY ./app /app 

WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /temp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp /temp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user
