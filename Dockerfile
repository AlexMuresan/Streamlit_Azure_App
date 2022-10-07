# This is the base image that will be used to create the docker image
FROM mambaorg/micromamba:0.27.0
# Exposes port 8501 to have access to streamlit UI
EXPOSE 8501

USER root
RUN apt-get update && DEBIAN_FRONTEND=“noninteractive” apt-get install -y --no-install-recommends \
       nginx \
       ca-certificates \
       apache2-utils \
       certbot \
       python3-certbot-nginx \
       sudo \
       cifs-utils \
       && \
    rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get -y install cron
RUN mkdir /opt/streamlit_azure
RUN chmod -R 777 /opt/streamlit_azure
WORKDIR /opt/streamlit_azure

USER $MAMBA_USER
# Copy files from local to docker image
# environment.yml - for conda env init
# run.sh - script that starts the streamlit app and ngninx
# nginx.conf - config for nginx
COPY environment.yml environment.yml
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes
COPY run.sh run.sh
COPY Streamlit-App Streamlit-App
COPY nginx.conf /etc/nginx/nginx.conf
# copy ooperations finished here

USER root
# change permissions of run.sh
RUN chmod a+x run.sh
# runs this command inside the container
CMD ["./run.sh"]