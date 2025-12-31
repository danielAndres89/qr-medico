from app import create_app
from app import crear_admin_por_defecto

app = create_app()

with app.app_context():
    crear_admin_por_defecto()

if __name__ == "__main__":
    app.run()
