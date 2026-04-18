# -------------------------------------------------------
# FRAGMENTO PARA app.py
# -------------------------------------------------------
# 1. En la clase Project, añade este campo después de 'results':
#
#       images = db.Column(db.Text)  # URLs separadas por comas, máx 5
#
# -------------------------------------------------------
# 2. Función auxiliar — añádela después de track_visit()
#    Recoge las 5 URLs del formulario y las une en un string.
#    Filtra las que vengan vacías para no guardar comas de más.

def collect_images_from_form() -> str:
    """
    Recoge image_1 … image_5 del formulario POST,
    descarta los vacíos y devuelve un string separado por comas.
    Ejemplo resultado: "https://raw.github.../g1.png,https://..."
    """
    urls = []
    for i in range(1, 6):
        url = request.form.get(f"image_{i}", "").strip()
        if url:
            urls.append(url)
    return ",".join(urls)


# -------------------------------------------------------
# 3. En panel_create_project, dentro del if request.method == "POST":
#    Añade images=collect_images_from_form() al Project():
#
#    db.session.add(Project(
#        title=...,
#        ...
#        results=request.form.get("results"),
#        images=collect_images_from_form(),   # <-- AÑADIR ESTO
#    ))
#
# -------------------------------------------------------
# 4. En panel_edit_project, dentro del if request.method == "POST":
#    Añade esta línea junto a las demás asignaciones:
#
#    project.images = collect_images_from_form()   # <-- AÑADIR ESTO
#
# -------------------------------------------------------
# 5. Mismo cambio para admin_create_project y admin_edit_project
#    si también los usas (aunque el panel nuevo los reemplaza).
# -------------------------------------------------------
