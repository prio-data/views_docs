FROM views3/uvicorn-deployment:2.1.0

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY ./viewsdocs/* /viewsdocs/
ENV GUNICORN_APP="viewsdocs.app:app"
