"""
migrate_add_sender_ip.py

Añade la columna 'sender_ip' a la tabla contact_message
para el sistema de rate limiting anti-spam.
Seguro de ejecutar múltiples veces.
"""

import os
from dotenv import load_dotenv

load_dotenv()

from app import app, db
from sqlalchemy import text

with app.app_context():
    with db.engine.connect() as conn:
        try:
            conn.execute(text(
                "ALTER TABLE contact_message ADD COLUMN IF NOT EXISTS sender_ip VARCHAR(64);"
            ))
            conn.commit()
            print("✅ Columna 'sender_ip' añadida (o ya existía)")
        except Exception as e:
            print(f"⚠️  Error: {e}")

    print("\n✅ Migración completada.")
