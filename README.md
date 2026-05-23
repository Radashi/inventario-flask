# Sistema de Inventario Web - Proyecto Extraordinario

## Descripción del Proyecto

Este proyecto es una aplicación web funcional desarrollada con Python y Flask para la administración de un inventario de productos. El sistema permite gestionar usuarios y productos mediante operaciones CRUD completas, cuenta con un sistema de autenticación seguro, una API REST nativa para integraciones externas, cobertura de pruebas automatizadas y está completamente dockerizado para facilitar su despliegue.

## Tecnologías Utilizadas

- **Backend:** Python 3.12, Flask
- **Base de Datos:** MySQL (con `mysql-connector-python`)
- **Frontend:** HTML5, Bootstrap 5, Jinja2
- **Pruebas Automatizadas:** Pytest
- **DevOps:** Docker, Git/GitHub
- **Herramientas de API:** HTTPie

## Instalación y Configuración Local

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TU_USUARIO/sistema-inventario-flask.git](https://github.com/TU_USUARIO/sistema-inventario-flask.git)
   cd sistema-inventario-flask
   ```
   Crear y activar el entorno virtual:

````Bash

    python3 -m venv venv
    source venv/bin/activate```

    Instalar dependencias:
```    Bash

    pip install -r requirements.txt```

*Configuración de la Base de Datos*

    Asegúrate de tener MySQL ejecutándose en tu sistema. Abre tu gestor de base de datos o terminal de MySQL. Ejecuta el script proporcionado en la raíz del proyecto para crear la base de datos y poblarla con datos de prueba:

```bash
    source bd_extraordinario_web.sql
````

    Nota: Si tu usuario de MySQL no es root o si tienes contraseña, actualiza las credenciales en el bloque de configuración del archivo app.py.

Ejecución del Sistema
Método 1: Servidor Local de Desarrollo

Con el entorno virtual activado y la base de datos configurada, ejecuta:

````Bash

python3 app.py```

La aplicación estará disponible en: http://127.0.0.1:5000
*(Método 2: Mediante Docker (Recomendado))*

Para desplegar la aplicación dentro de un contenedor aislado, utiliza los siguientes comandos:

    Construir la imagen:
 ```   Bash

    docker build -t app_extraordinario .

    Ejecutar el contenedor:
    Bash

    docker run -d --network host --name mi_contenedor_flask app_extraordinario
````

Nota: Se utiliza --network host para que el contenedor tenga acceso a la base de datos MySQL alojada en la máquina anfitriona local.
Uso de la API REST y Pruebas El sistema incluye una API REST en la ruta /api/productos. Puedes probarla fácilmente usando herramientas de terminal como httpie:
Bash

# Consultar todos los productos

http GET [http://127.0.0.1:5000/api/productos](http://127.0.0.1:5000/api/productos)

Para ejecutar la suite de pruebas automatizadas, simplemente corre el siguiente comando en la raíz del proyecto:
Bash

`pytest`
