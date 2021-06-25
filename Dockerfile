FROM alpine/git AS asyncpg-branch 
RUN git clone -b sslparams --recurse-submodules https://github.com/jdobes/asyncpg /asyncpg

FROM python:3.8
COPY requirements.txt /
COPY --from=asyncpg-branch /asyncpg /asyncpg/
RUN pip install /asyncpg
RUN pip install -r requirements.txt

RUN sed 's/SECLEVEL=[0-9]/SECLEVEL=1/g' /etc/ssl/openssl.cnf > /etc/ssl/openssl.cnf

COPY *.py / 
COPY ./viewsdocs/* /viewsdocs/
CMD ["python","init.py"]
