import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app

@pytest.fixture
def client():
    # Creamos la aplicación usando la "factory" que configuramos en app.py
    app = create_app()

    # Habilitamos el modo de pruebas (esto cambia cómo Flask maneja errores)
    app.config['TESTING'] = True

    # IMPORTANTE: En un proyecto real, aquí conectaríamos a una BD de pruebas
    # (ej. bd_extraordinario_test). Para esta tarea escolar, usaremos la misma,
    # pero debes tener cuidado de no borrar datos importantes.

    # Flask provee un 'test_client' que simula un navegador
    with app.test_client() as client:
        # El código aquí se ejecuta antes de cada prueba (setup)
        yield client
        # El código después del yield se ejecuta al terminar cada prueba (teardown)
