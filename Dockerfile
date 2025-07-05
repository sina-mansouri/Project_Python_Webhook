FROM python:3-slim

# Copy in your requirements file
ADD requirements.txt /requirements.txt


RUN set -ex \

    && BUILD_DEPS=" \

    build-essential \

    gosu \

    curl \

    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --no-cache-dir -r /requirements.txt \
    \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code/data

WORKDIR /code/

### nach install gunicorn
COPY app /code/app/
ADD docker /code/docker/
#####

ADD app /code/

COPY docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

#VOLUME /code/data

ENTRYPOINT ["/docker-entrypoint.sh"]

#CMD [ "python", "webhook_code.py" ]

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app.webhook_code:app"]
