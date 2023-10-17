FROM jupyter/base-notebook
WORKDIR /home/jovyan/work
COPY ./requirements.txt /home/jovyan/work
RUN python -m pip install --no-cache -r requirements.txt
