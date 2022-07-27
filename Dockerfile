FROM python:3.9.5

ENV PYTHONUNBUFFERED=1

WORKDIR /opt/back_end

COPY . .

RUN pip install -r requirements.txt

# Dejamos las variables definidas para un entorno de desarrollo, 
# debemos remplazarlas para un entorno productivo
ENV POSTGRES_DB=marvel_db
ENV POSTGRES_USER=inove_user
ENV POSTGRES_PASSWORD=123Marvel!
ENV POSTGRES_HOST=db

# Dejamos DEBUG=True para hacer los retoques antes de pasarlo a False para producción.
ENV DEBUG=True
ENV SECRET_KEY=django-insecure-$dpguq$#6!6dw($(qd6))7qcw%%#a=sc!-!7t!_av9%5*(q=uf
RUN python marvel/manage.py collectstatic --noinput
# CMD gunicorn --chdir /opt/back_end/marvel marvel.wsgi:application --bind 0.0.0.0:$PORT
CMD python marvel/manage.py 0.0.0.0:8000