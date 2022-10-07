FROM mambaorg/micromamba:0.27.0
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
COPY environment.yml environment.yml
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes
COPY run.sh run.sh
COPY Streamlit-App Streamlit-App
COPY nginx.conf /etc/nginx/nginx.conf

USER root
RUN chmod a+x run.sh
CMD ["./run.sh"]