from flask import Flask, redirect, url_for
from controllers.auth_controller import auth_bp
from controllers.producto_controller import producto_bp
from controllers.api_controller import api_bp

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'      # usuario de MySQL
    app.config['MYSQL_PASSWORD'] = ''      # contraseña de MySQL
    app.config['MYSQL_DB'] = 'bd_extraordinario_web'

    # llave secreta para manejar las sesiones del login
    app.config['SECRET_KEY'] = '1234'

    # Registro de controladores
    app.register_blueprint(auth_bp)
    app.register_blueprint(producto_bp)
    app.register_blueprint(api_bp)
    @app.route('/')
    def root():
        return redirect(url_for('auth.login'))

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
