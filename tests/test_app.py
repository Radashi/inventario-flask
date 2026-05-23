def test_inicio_sesion(client):
    """Prueba 1: Evaluar que el inicio de sesión funcione correctamente."""

    # Hacemos un POST a la ruta de login con credenciales válidas
    respuesta = client.post('/login', data={
        'correo': 'juan@empresa.com',
        'password': 'admin123'
    }, follow_redirects=True) # follow_redirects=True le dice a Flask que siga la redirección al dashboard/productos

    # Verificamos que la página resultante sea la de los productos
    assert respuesta.status_code == 200
    # Verificamos que el HTML contenga texto que solo se ve al iniciar sesión
    assert b'Inventario de Productos' in respuesta.data
    assert b'Juan P\xc3\xa9rez' in respuesta.data # \xc3\xa9 es la 'é' codificada

def test_consulta_productos_api(client):
    """Prueba 2: Evaluar la consulta de productos (usando nuestra API)."""

    # Hacemos un GET a la ruta de la API
    respuesta = client.get('/api/productos')

    # Verificamos que el código HTTP sea 200 (OK)
    assert respuesta.status_code == 200

    # Convertimos la respuesta JSON a una lista de diccionarios en Python
    data = respuesta.get_json()

    # Verificamos que lo que recibimos sea una lista (el arreglo de productos)
    assert isinstance(data, list)

def test_insercion_producto(client):
    """Prueba 3: Evaluar la inserción de un producto nuevo vía POST."""

    # Primero necesitamos iniciar sesión porque la ruta web está protegida.
    # Con el test_client de Flask, la sesión se mantiene entre peticiones.
    client.post('/login', data={
        'correo': 'juan@empresa.com',
        'password': 'admin123'
    })

    # Ahora hacemos el POST a la ruta de agregar producto
    respuesta = client.post('/productos/agregar', data={
        'nombre': 'Producto de Prueba Pytest',
        'descripcion': 'Generado por automatización',
        'precio': '99.99',
        'stock': '5'
    }, follow_redirects=True)

    # Verificamos que la página cargó correctamente
    assert respuesta.status_code == 200

    # Verificamos que el mensaje de éxito y el nombre del producto estén en el HTML devuelto
    assert b'Producto agregado correctamente' in respuesta.data
    assert b'Producto de Prueba Pytest' in respuesta.data
