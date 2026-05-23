from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.db import get_db_connection

auth_bp = Blueprint('auth', __name__)

# Esta ruta maneja tanto mostrar el formulario (GET) como recibir los datos (POST)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener los datos del formulario HTML
        correo = request.form['correo']
        password_ingresada = request.form['password']

        # Coneccion a la base de datos
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True) # dictionary=True  devuelve los resultados como diccionario mas facil de leer pues

        # Buscar al usuario por correo
        # Vi que se usa %s para evitar un ataque llamado SQL Injection asi que se lo pongo como extra
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        usuario = cursor.fetchone()

        # Cerramos la conexión
        cursor.close()
        conexion.close()

        # Validar las credenciales
        # Si el usuario existe y la contraseña coincide
        if usuario and usuario['password'] == password_ingresada:
            # Iniciamos sesión guardando datos en el objeto 'session'
            session['id_usuario'] = usuario['id_usuario']
            session['nombre'] = usuario['nombre']

            # Redirigimos al panel de productos
            return redirect(url_for('producto.index'))
        else:
            # Si falla, muestra un mensaje de error usando flash
            flash('Correo o contraseña incorrectos.')
            return redirect(url_for('auth.login'))

    # Si la petición es GET mostramos el HTML
    return render_template('login.html')

# Ruta para cerrar sesión
@auth_bp.route('/logout')
def logout():
    session.clear() # Borramos todo lo de la sesión
    return redirect(url_for('auth.login'))
