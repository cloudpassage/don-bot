# Get the halocelery component
FROM docker.io/halotools/python-sdk:ubuntu-18.04_sdk-latest_py-3.6 as downloader
MAINTAINER toolbox@cloudpassage.com

ARG HALOCELERY_BRANCH=v0.9.1

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        git

WORKDIR /app/

RUN echo "Target branch for this build: $HALOCELERY_BRANCH"

RUN git clone -b $HALOCELERY_BRANCH https://github.com/cloudpassage/halocelery

RUN cd halocelery && \
    git archive \
        --verbose \
        --format=tar.gz \
        -o /app/halocelery.tar.gz \
        $HALOCELERY_BRANCH

#####################################
# Unit and integration tests run in a separate step.

FROM docker.io/halotools/python-sdk:ubuntu-18.04_sdk-latest_py-3.6
MAINTAINER toolbox@cloudpassage.com

ENV SLACK_ICON_URL='http://www.cloudpassage.com/wp-content/uploads/2016/12/don-operator.png'
ENV HALO_API_HOSTNAME='api.cloudpassage.com'
ENV HALO_API_PORT='443'

# These arguments allow integration testing with the Halo API
ARG HALO_API_KEY
ARG HALO_API_SECRET_KEY

ARG DEBIAN_FRONTEND=noninteractive

# Up to root to add additional packages
USER root

RUN apt-get update && \
    apt-get install -y \
        curl \
        expect \
        git

# Drop in the app code
COPY . /app/

# Setup for manual library installation
RUN mkdir /src/
WORKDIR /src/

COPY --from=downloader /app/halocelery.tar.gz /src/halocelery/halocelery.tar.gz

RUN cd halocelery && \
    tar -zxvf ./halocelery.tar.gz && \
    cd /src/ && \
    mv ./halocelery /app/app/


WORKDIR /app/app

RUN pip3 install -r requirements-test.txt

# Now take ownership and drop to non-root user
RUN chown -R ${APP_USER}:$APP_GROUP /app

USER ${APP_USER}

#####################################
# Building the final container image

FROM docker.io/halotools/python-sdk:ubuntu-18.04_sdk-latest_py-3.6
MAINTAINER toolbox@cloudpassage.com

ENV SLACK_ICON_URL='http://www.cloudpassage.com/wp-content/uploads/2016/12/don-operator.png'
ENV HALO_API_HOSTNAME='api.cloudpassage.com'
ENV HALO_API_PORT='443'

ARG DEBIAN_FRONTEND=noninteractive

# Up to root to add additional packages
USER root

RUN apt-get update && \
    apt-get install -y \
        expect

# Drop in the app code
COPY app/ /app/

# Setup for manual library installation
RUN mkdir /src/
WORKDIR /src/


COPY --from=downloader /app/halocelery.tar.gz /src/halocelery/halocelery.tar.gz

RUN cd halocelery && \
    tar -zxvf ./halocelery.tar.gz && \
    cd /src/ && \
    mv ./halocelery /app


WORKDIR /app

RUN pip3 install -r requirements.txt

# Now take ownership and drop to non-root user
RUN chown -R ${APP_USER}:$APP_GROUP /app

USER ${APP_USER}

WORKDIR /app

CMD ["unbuffer", "python3", "/app/runner.py"]
