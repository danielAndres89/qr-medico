from app import create_app
from app.init_db import init_db

app = create_app()

# 🔹 CREA LAS TABLAS SI NO EXISTEN
init_db(app)

if __name__ == "__main__":
    app.run()
