FROM alpine:3.4
MAINTAINER toolbox@cloudpassage.com

ENV SLACK_ICON_URL=https://pbs.twimg.com/profile_images/803676842599157760/JULYcky5_400x400.jpg
ENV HALO_API_HOSTNAME=api.cloudpassage.com
ENV HALO_API_PORT=443

RUN apk add --no-cache \
    git=2.8.3-r0 \
    python=2.7.12-r0 \
    py-pip=8.1.2-r0

COPY app/ /app/

WORKDIR /app

RUN pip install -r requirements.txt

RUN py.test --cov=donlib

CMD /app/runner.py
