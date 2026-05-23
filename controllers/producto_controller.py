from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.db import get_db_connection

# Creamos un nuevo Blueprint para los productos
producto_bp = Blueprint('producto', __name__)

# Ruta para LISTAR los productos (Leer)
@producto_bp.route('/productos')
def index():
    # Proteger la ruta: si no hay sesión, lo mandamos al login
    if 'id_usuario' not in session:
        return redirect(url_for('auth.login'))

    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)

    # Consultamos todos los productos
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    # Le pasamos la lista de productos y el nombre del usuario a la vista
    return render_template('productos.html', productos=productos, nombre_usuario=session['nombre'])

# Ruta para AGREGAR un producto (Crear)
@producto_bp.route('/productos/agregar', methods=['POST'])
def agregar():
    if 'id_usuario' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']

        # --- VALIDACIONES (Como lo pide tu rúbrica) ---
        if not nombre or not precio or not stock:
            flash('Error: El nombre, precio y stock son obligatorios.', 'danger')
            return redirect(url_for('producto.index'))

        if float(precio) <= 0:
            flash('Error: El precio debe ser mayor a cero.', 'danger')
            return redirect(url_for('producto.index'))

        if int(stock) < 0:
            flash('Error: El stock no puede ser negativo.', 'danger')
            return redirect(url_for('producto.index'))

        # Si pasa las validaciones, lo guardamos en la BD
        conexion = get_db_connection()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)",
            (nombre, descripcion, precio, stock)
        )
        conexion.commit() # Guardamos los cambios

        cursor.close()
        conexion.close()

        flash('Producto agregado correctamente.', 'success')
        return redirect(url_for('producto.index'))

# Ruta para ELIMINAR un producto
@producto_bp.route('/productos/eliminar/<int:id>')
def eliminar(id):
    if 'id_usuario' not in session:
        return redirect(url_for('auth.login'))

    conexion = get_db_connection()
    cursor = conexion.cursor()

    # Eliminamos el producto donde el ID coincida
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('producto.index'))

# Ruta para MOSTRAR el formulario de EDICIÓN
@producto_bp.route('/productos/editar/<int:id>')
def editar(id):
    if 'id_usuario' not in session:
        return redirect(url_for('auth.login'))

    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)

    # Buscamos los datos actuales del producto
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    # Si por alguna razón el producto no existe, regresamos al index
    if not producto:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('producto.index'))

    # Creamos una nueva plantilla para la edición (la haremos en el siguiente paso)
    return render_template('editar_producto.html', producto=producto)

# Ruta para PROCESAR la ACTUALIZACIÓN
@producto_bp.route('/productos/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    if 'id_usuario' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']

        # Validaciones (las mismas que usamos al agregar)
        if not nombre or not precio or not stock:
            flash('Error: El nombre, precio y stock son obligatorios.', 'danger')
            return redirect(url_for('producto.editar', id=id))

        if float(precio) <= 0:
            flash('Error: El precio debe ser mayor a cero.', 'danger')
            return redirect(url_for('producto.editar', id=id))

        if int(stock) < 0:
            flash('Error: El stock no puede ser negativo.', 'danger')
            return redirect(url_for('producto.editar', id=id))

        conexion = get_db_connection()
        cursor = conexion.cursor()

        # Actualizamos la base de datos
        cursor.execute(
            """
            UPDATE productos
            SET nombre = %s, descripcion = %s, precio = %s, stock = %s
            WHERE id_producto = %s
            """,
            (nombre, descripcion, precio, stock, id)
        )
        conexion.commit()

        cursor.close()
        conexion.close()

        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('producto.index'))
