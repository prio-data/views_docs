FROM prioreg.azurecr.io/uvicorn-deployment 

COPY requirements.txt /
RUN pip install -r requirements.txt

#COPY --from=asyncpg-branch /asyncpg /asyncpg/
#RUN pip install --upgrade /asyncpg

RUN sed 's/SECLEVEL=[0-9]/SECLEVEL=1/g' /etc/ssl/openssl.cnf > /etc/ssl/openssl.cnf

COPY ./viewsdocs/* /viewsdocs/
ENV APP="viewsdocs.app:app"

COPY ensure_certs.py / 
COPY init.sh / 
CMD ["bash","init.sh"]
