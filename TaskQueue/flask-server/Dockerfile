FROM python:3.12-slim

# layer caching for faster builds
COPY requirements.txt /
RUN pip install -r /requirements.txt

#COPY app.py /app.py
ADD . /flask-server
WORKDIR /flask-server

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

CMD flask run --host=0.0.0.0

#CMD gunicorn --workers $WORKERS \
#  --threads $THREADS \
#  --bind 0.0.0.0:$PORT_APP \
#  --log-level DEBUG \
#  app:app