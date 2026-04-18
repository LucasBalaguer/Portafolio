"""
migrate_add_images.py

Añade la columna 'images' a la tabla project.
Guarda hasta 5 URLs de imágenes separadas por comas.
Seguro de ejecutar múltiples veces (usa IF NOT EXISTS).
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
                "ALTER TABLE project ADD COLUMN IF NOT EXISTS images TEXT;"
            ))
            conn.commit()
            print("✅ Columna 'images' añadida (o ya existía)")
        except Exception as e:
            print(f"⚠️  Error: {e}")

    print("\n✅ Migración completada.")
