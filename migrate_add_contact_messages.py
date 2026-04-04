"""
migrate_add_contact_messages.py

Añade la tabla contact_message a Supabase.
Seguro de ejecutar múltiples veces (usa IF NOT EXISTS).
"""

import os
from dotenv import load_dotenv

load_dotenv()

from app import app, db

with app.app_context():
    db.create_all()
    print("✅ Tabla contact_message creada (o ya existía).")
    print("✅ Migración completada.")
