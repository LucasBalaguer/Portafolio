# -------------------------------------------------------
# AÑADIR EN app.py — justo antes de las páginas de error
# -------------------------------------------------------
# Estas dos rutas sirven el sitemap.xml y robots.txt
# directamente desde Flask sin necesidad de archivos estáticos.
#
# El sitemap genera automáticamente las URLs de los proyectos
# desde la base de datos, por eso no puede ser un archivo estático.
# -------------------------------------------------------

from flask import Response  # añadir este import al bloque de imports del principio

@app.route("/sitemap.xml")
def sitemap():
    """
    Genera el sitemap.xml dinámicamente.
    Las páginas fijas están hardcodeadas.
    Los proyectos se obtienen de la BD para que se actualicen solos.
    """
    # URL base del sitio — cámbiala si cambias de dominio
    base_url = "https://www.lucascavalcante.es"

    # Páginas fijas con su prioridad y frecuencia de cambio
    static_pages = [
        {"url": "/",          "priority": "1.0", "changefreq": "weekly"},
        {"url": "/sobre-mi",  "priority": "0.9", "changefreq": "monthly"},
        {"url": "/proyectos", "priority": "0.9", "changefreq": "weekly"},
        {"url": "/skills",    "priority": "0.7", "changefreq": "monthly"},
        {"url": "/contacto",  "priority": "0.6", "changefreq": "yearly"},
    ]

    # Páginas dinámicas — proyectos
    projects = Project.query.all()

    # Construimos el XML manualmente (no necesita librerías externas)
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for page in static_pages:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{base_url}{page['url']}</loc>")
        xml_lines.append(f"    <changefreq>{page['changefreq']}</changefreq>")
        xml_lines.append(f"    <priority>{page['priority']}</priority>")
        xml_lines.append("  </url>")

    for project in projects:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{base_url}/projects/{project.slug}</loc>")
        xml_lines.append("    <changefreq>monthly</changefreq>")
        xml_lines.append("    <priority>0.8</priority>")
        xml_lines.append("  </url>")

    xml_lines.append("</urlset>")

    xml_content = "\n".join(xml_lines)

    # Devolvemos el XML con el content-type correcto para que
    # Google lo reconozca como sitemap
    return Response(xml_content, mimetype="application/xml")


@app.route("/robots.txt")
def robots():
    """
    Sirve el robots.txt.
    Allow: / → permite indexar todo el sitio.
    Disallow: /panel/ → bloquea el panel privado.
    Disallow: /admin/ → bloquea el admin legacy.
    Sitemap → le dice a Google dónde está el sitemap.
    """
    content = """User-agent: *
Allow: /
Disallow: /panel/
Disallow: /admin/

Sitemap: https://www.lucascavalcante.es/sitemap.xml
"""
    return Response(content, mimetype="text/plain")
