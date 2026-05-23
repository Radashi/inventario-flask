from flask import Blueprint, jsonify, request
from models.db import get_db_connection

# Usamos url_prefix para que todas las rutas de este archivo empiecen con /api automáticamente
api_bp = Blueprint('api', __name__, url_prefix='/api')

# GET: Consultar todos los productos
@api_bp.route('/productos', methods=['GET'])
def get_productos():
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    # MySQL devuelve los decimales en un formato que JSON no entiende directamente.
    # Convertimos el precio a float para evitar errores.
    for p in productos:
        p['precio'] = float(p['precio'])

    return jsonify(productos), 200 # 200 significa "OK"

# POST: Registrar un nuevo producto
@api_bp.route('/productos', methods=['POST'])
def crear_producto():
    # En una API, los datos llegan en el "cuerpo" (body) de la petición como JSON
    datos = request.get_json()

    # Manejo de errores básico: verificar que enviaron la información
    if not datos or not 'nombre' in datos or not 'precio' in datos or not 'stock' in datos:
        return jsonify({"error": "Faltan datos obligatorios (nombre, precio, stock)."}), 400 # 400 = Bad Request

    conexion = get_db_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)",
            (datos['nombre'], datos.get('descripcion', ''), datos['precio'], datos['stock'])
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid # Obtenemos el ID del producto recién creado
    except Exception as e:
        return jsonify({"error": str(e)}), 500 # 500 = Error interno del servidor
    finally:
        cursor.close()
        conexion.close()

    return jsonify({"mensaje": "Producto creado con éxito", "id": nuevo_id}), 201 # 201 = Creado

# PUT: Actualizar un producto existente
@api_bp.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "No se enviaron datos para actualizar."}), 400

    conexion = get_db_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, stock = %s WHERE id_producto = %s",
            (datos['nombre'], datos.get('descripcion', ''), datos['precio'], datos['stock'], id)
        )
        conexion.commit()

        # Validamos si realmente se modificó alguna fila
        if cursor.rowcount == 0:
            return jsonify({"error": "Producto no encontrado."}), 404 # 404 = Not Found

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conexion.close()

    return jsonify({"mensaje": "Producto actualizado correctamente"}), 200

# DELETE: Eliminar un producto
@api_bp.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    conexion = get_db_connection()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
    conexion.commit()
    filas_afectadas = cursor.rowcount

    cursor.close()
    conexion.close()

    if filas_afectadas == 0:
        return jsonify({"error": "Producto no encontrado."}), 404

    return jsonify({"mensaje": "Producto eliminado correctamente"}), 200
