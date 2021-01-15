FROM jupyter/scipy-notebook:42f4c82a07ff

LABEL maintainer="max.schroeder@uni-rostock.de"

# Copy requirements file from host to temp directory
COPY requirements.txt /tmp/requirements.txt

# Install requirements
RUN python3 -m pip install -r /tmp/requirements.txt

USER root

# Enable Jupyter extensions
RUN jupyter contrib nbextension install --system

# Enable Jupyter extensions
RUN jupyter nbextension enable toc2/main --system && \
    jupyter nbextension enable --py latex_envs --system && \
    jupyter nbextension enable spellchecker/main --system && \
    jupyter nbextension enable execute_time/ExecuteTime --system && \
    jupyter nbextension enable varInspector/main --system

# Set user to Jupyter Notebook user
USER $NB_USER

# Change working directory to volume mount point
WORKDIR /home/$NB_USER/work
