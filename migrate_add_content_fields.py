"""
migrate_add_content_fields.py

Añade las columnas 'problem', 'process' y 'results' a la tabla project
en Supabase (o cualquier PostgreSQL). Seguro de ejecutar múltiples veces.
"""

import os
from dotenv import load_dotenv

load_dotenv()

from app import app, db
from sqlalchemy import text

with app.app_context():
    with db.engine.connect() as conn:
        for column in ["problem", "process", "results"]:
            try:
                conn.execute(text(
                    f"ALTER TABLE project ADD COLUMN IF NOT EXISTS {column} TEXT;"
                ))
                conn.commit()
                print(f"✅ Columna '{column}' añadida (o ya existía)")
            except Exception as e:
                print(f"⚠️  Error con '{column}': {e}")

    print("\n✅ Migración completada. Ya puedes editar los proyectos con el nuevo contenido.")
