import os
from dotenv import load_dotenv

load_dotenv()

from app import app, db, Project

with app.app_context():

    # ----------------------------
    # PROYECTO 1 — EDA Vivienda y Paro
    # ----------------------------
    p1 = Project(
        title="EDA Evolución Vivienda y Paro en España",
        slug="eda-vivienda-paro-espana",
        description=(
            "Análisis exploratorio de la evolución del precio de la vivienda "
            "y la tasa de paro en España entre 2014 y 2024, estudiando su relación "
            "por comunidad autónoma y extrayendo conclusiones sobre rentabilidad "
            "de compra frente a alquiler."
        ),
        role="Data Analyst",
        tech="Python, Pandas, NumPy, Matplotlib, Seaborn, SciPy",
        duration="4 semanas",
        github="https://github.com/SandraGM1/EDA_Evolucion_Vivienda_Paro_Espana"
    )

    # ----------------------------
    # PROYECTO 2 — ML Infracciones de Tráfico
    # ----------------------------
    p2 = Project(
        title="Predicción de Gravedad en Infracciones de Tráfico",
        slug="ml-infracciones-trafico",
        description=(
            "Modelo de clasificación binaria para predecir si una infracción de "
            "tráfico es grave o no, permitiendo a aseguradoras ajustar primas de "
            "riesgo. Modelo final: LightGBM optimizado con ajuste de umbral, "
            "alcanzando un recall del 64% en la clase grave."
        ),
        role="Data Scientist",
        tech="Python, Pandas, Scikit-learn, LightGBM, XGBoost, Seaborn, Matplotlib",
        duration="3 semanas",
        github="https://github.com/LucasBalaguer/ML_Infracciones_de_trafico"
    )

    # ----------------------------
    # Insertar evitando duplicados
    # ----------------------------
    existing_slugs = [p.slug for p in Project.query.all()]

    added = []
    for project in [p1, p2]:
        if project.slug not in existing_slugs:
            db.session.add(project)
            added.append(project.title)

    db.session.commit()

    if added:
        print(f"✅ Proyectos añadidos: {', '.join(added)}")
    else:
        print("⚠️  Los proyectos ya existían en la base de datos.")
