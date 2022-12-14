FROM python:3.9.5

ENV PYTHONUNBUFFERED=1

WORKDIR /opt/backend

COPY . .

RUN apt -y update && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

RUN mkdir /opt/backend/marvel/logs

# Environment variables for local development
ENV POSTGRES_DB=inove
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=ics2022ma-
ENV POSTGRES_HOST=db
ENV SECRET_KEY=django-insecure-x_^aet@$di37)k$5vb(kino$6w=px!&@-q4va4so^2c9s@)k8*

# Dejamos DEBUG=True para hacer los retoques antes de pasarlo a False para producción.
ENV DEBUG=True

RUN python marvel/manage.py collectstatic --noinput

CMD gunicorn --chdir /opt/backend/marvel marvel.wsgi:application --bind 0.0.0.0:$PORT