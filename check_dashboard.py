# check_dashboard.py
from dotenv import load_dotenv
load_dotenv()

from app import app, db
from sqlalchemy import text

with app.app_context():
    with db.engine.connect() as conn:
        r = conn.execute(text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'project' ORDER BY ordinal_position;"
        ))
        cols = [row[0] for row in r]
        print("Columnas:", cols)
        print("\n¿dashboard_url existe?", "dashboard_url" in cols)