from flask import Flask
from .config import Config
from .extensions import db, login_manager, bcrypt, migrate
from app.personas.routes import personas_bp
from app.models import Usuario
from app.extensions import db, bcrypt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)  # 👈 ESTA LÍNEA CREA "flask db"

    login_manager.login_view = "auth.login"

    from .auth.routes import auth_bp
    from .personas.routes import personas_bp
    from .qr.routes import qr_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(personas_bp)
    app.register_blueprint(qr_bp)

    return app


def crear_admin_por_defecto():
    admin = Usuario.query.filter_by(username="admin").first()
    if not admin:
        admin = Usuario(
            username="admin",
            password_hash=bcrypt.generate_password_hash("admin123").decode(),
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario admin creado")
