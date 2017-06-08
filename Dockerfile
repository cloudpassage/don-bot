FROM alpine:3.4
MAINTAINER toolbox@cloudpassage.com

ENV SLACK_ICON_URL=http://www.cloudpassage.com/wp-content/uploads/2016/12/don-operator.png
ENV HALO_API_HOSTNAME=api.cloudpassage.com
ENV HALO_API_PORT=443
ENV APP_USER=donbot
ENV APP_GROUP=botgroup

COPY app/ /app/
COPY .git/ /.git/

RUN addgroup ${APP_GROUP} && \
    adduser \
        -D \
        -G ${APP_GROUP} \
        -s /bin/sh \
        -h /app \
        ${APP_USER} && \
    apk add --no-cache \
        git=2.8.5-r0 \
        python=2.7.12-r0 \
        py-pip=8.1.2-r0 && \
    pip install -r /app/requirements.txt && \
    py.test --flake8 --cov=donlib /app/test && \
    chown -R ${APP_USER}:${APP_GROUP} /app

WORKDIR /app

WORKDIR /app

USER ${APP_USER}

CMD /app/runner.py
