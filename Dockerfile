FROM prioreg.azurecr.io/prio-data/uvicorn_deployment:1.3.0

COPY requirements.txt /
RUN pip install -r requirements.txt

RUN sed 's/SECLEVEL=[0-9]/SECLEVEL=1/g' /etc/ssl/openssl.cnf > /etc/ssl/openssl.cnf

COPY ./viewsdocs/* /viewsdocs/
ENV APP="viewsdocs.app:app"
