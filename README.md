# Streamlit App on Azure

## Files

- **Dockerfile**
  - contains instructions on how the docker image should be created
  - building the image is done using the `docker build -t $IMAGE_NAME:$IMAGE_VERSION .` command
    - e.g. `docker build -t streamlit_azure:v1 .`
    - more info inside the file
    - shouldn't need any changes
- **environment.yml**
  - used to initialise the conda environment and install dependencies
  - shoudln't need any changes
- **deployment.yml**
  - information for azure deployment
  - change password on line 21 with the one you get using these commands
    - `az acr login -n bpdsregistry`
    - `az acr update -n bpdsregistry --admin-enabled true`
    - `az acr credential show --name  bpdsregistry`
  - The `dnsNameLabel` on line 30 refers to what you would like your domain name to be — this app should be able to be accessed using `streamlit_azure.westus.azurecontainer.io` after it's deployed.
- **nginx.conf**
  - used to configure nginx
  - `server name` should be changed in case `dnsNameLabel` is changed in `deployment.yml`
    - format is `dnsNameLabel.location.azurecontainer.io` where `dnsNameLabel` and `location` are the same as in `deployment.yml`
- **run.sh**
  - starts `nginx` and the streamlit app
  - needs to `cd` inside `Streamlit-App` because otherwise the custom theme inside `Streamlit-App/.streamlit/config.toml` is not applied.
  - `server.port` and `server.address` params are specified for reproducibility.

## Running Locally

In order to test the Docker image locally you can run the following commands

1. docker build -t streamlit_azure:v1 .
   1. to create an image called `streamlit_azure` with version `v1`
2. docker run -p 8501:8501 streamlit_azure:v1
   1. creates a container with the `streamlit_azure:v1` image and starts it.
   2. `-p` parameters maps a local port to the container port (first port is local, second is of container)
3. Open a browser window and access `localhost:8501` - the streamlit app should be here.

## Pushing image to Azure Container Registry and deploying the app

1. `az acr login -n bpdsregistry`
2. `docker build -t azure_demo:v1 .`
3. `docker tag streamlit_azure:v1 bpdsregistry.azurecr.io/streamlit_azure:v1`
4. `docker push bpdsregistry.azurecr.io/streamlit_azure:v1`
5. `az container create --resource-group bpds_poc --name streamlit_azure -f deployment.yml`

## Full length tutorial

The full length tutorial is at [this link](https://towardsdatascience.com/beginner-guide-to-streamlit-deployment-on-azure-f6618eee1ba9).

---

# Fileshare Volume

Some helpful commands to rebuild and launch application in azure. Some names should be changed for your particular image/etc.

Rebuild image and push to azure container registry repository

1. `docker build -t bpdsregistry.azurecr.io/azure_demo:v2 .`
2. `docker push bpdsregistry.azurecr.io/azure_demo:v2`


Deploy the image in an azure container

1. `az container create --resource-group bpds_poc --name streamlit_azure-2 -f deployment.yml`

Connect to a deployed container at bash prompt for exploration/debugging/etc

1. `az container exec --resource-group bpds_poc --name streamlit_azure-2 --exec-command “/bin/bash”`

 

