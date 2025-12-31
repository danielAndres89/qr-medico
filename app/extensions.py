from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()

@login_manager.user_loader
def load_user(user_id):
    from app.models import Usuario  # 👈 IMPORT LOCAL (CLAVE)
    return Usuario.query.get(int(user_id))