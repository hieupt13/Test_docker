FROM tiangolo/uwsgi-nginx-flask:python3.7
RUN pip install --upgrade pip
COPY requirement.txt /app/requirements.txt
RUN pip3 install  -r /app/requirements.txt
COPY collectors /app/collectors
COPY sql_db /app/sql_db
COPY settings.cfg /app/settings.cfg
COPY openapi /app/openapi
COPY docker/uwsgi.ini /app/uwsgi.ini
COPY app.py /app/
