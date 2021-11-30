FROM prioreg.azurecr.io/prio-data/uvicorn_deployment:2.0.0

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY ./viewsdocs/* /viewsdocs/
ENV GUNICORN_APP="viewsdocs.app:app"
