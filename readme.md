![Inove banner](inove.jpg)
Inove Escuela de C贸digo\
info@inove.com.ar\
Web: [Inove](http://inove.com.ar)

---

# Django - Backend - Marvel Comics Ecommerce
Esta aplicaci贸n fue creada para poder consumir el backend del ecommmerce de marvel v铆a requests.

---

## **Documentaci贸n de la API** 馃摎
Se puede acceder a la documentaci贸n de la API en el endpoint [`/api-docs/swagger`](https://inove-marvel-backend.herokuapp.com/api-docs/swagger) para **swagger-ui**, o tambi茅n [`/api-docs/redoc`](https://inove-marvel-backend.herokuapp.com/api-docs/redoc) para **redoc**.

--- 

## Comando 煤tiles 馃捇

### **Conectarse a contenedor remoto**
Podemos conectarnos al contenedor remoto con el comando:

```bash
$ heroku run bash
```

Luego debemos realizar los comandos habituales para la puesta en marcha de la aplicaci贸n en Django:

```bash
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
```

De ser necesario, podemos migrar espec铆ficamente la aplicaci贸n ecommerce, para crear los modelos de nuestra aplicaci贸n:

```bash
$ python manage.py makemigrations ecommerce
$ python manage.py migrate ecommerce
```

### **Observar los logs del sistema**
Para ver los logs de la aplicaci贸n, tenemos dos opciones:

```bash
$ heroku logs --tail
```

Nos permite ver los logs de la aplicaci贸n de Heroku, pero no los internos de Django, para ello debemos ejecutar el comando:

```
$ heroku run bash
$ cd marvel/logs
$ tail general-batch.log
```

---
## Consultas
alumnos@inove.com.ar