![Inove banner](inove.jpg)
Inove Escuela de Código\
info@inove.com.ar\
Web: [Inove](http://inove.com.ar)

---

# Django - Backend - Marvel Comics Ecommerce
Esta aplicación fue creada para poder consumir el backend del ecommmerce de marvel vía requests.

---

## **Documentación de la API** 📚
Se puede acceder a la documentación de la API en el endpoint [`/api-docs/swagger`](https://inove-marvel-backend.herokuapp.com/api-docs/swagger) para **swagger-ui**, o también [`/api-docs/redoc`](https://inove-marvel-backend.herokuapp.com/api-docs/redoc) para **redoc**.

--- 

## Comando útiles 💻

### **Conectarse a contenedor remoto**
Podemos conectarnos al contenedor remoto con el comando:

```bash
$ heroku run bash
```

Luego debemos realizar los comandos habituales para la puesta en marcha de la aplicación en Django:

```bash
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
```

De ser necesario, podemos migrar específicamente la aplicación ecommerce, para crear los modelos de nuestra aplicación:

```bash
$ python manage.py makemigrations ecommerce
$ python manage.py migrate ecommerce
```

### **Observar los logs del sistema**
Para ver los logs de la aplicación, tenemos dos opciones:

```bash
$ heroku logs --tail
```

Nos permite ver los logs de la aplicación de Heroku, pero no los internos de Django, para ello debemos ejecutar el comando:

```
$ heroku run bash
$ cd marvel/logs
$ tail general-batch.log
```

---
## Consultas
alumnos@inove.com.ar