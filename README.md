# Portafolio · Lucas Balaguer

Sitio web personal desarrollado desde cero con Flask, donde presento mis proyectos de análisis de datos y machine learning. Diseñado, construido y desplegado por mí — no es una plantilla ni un CMS.

🔗 **[lucascavalcante.es](https://lucascavalcante.es)**

---

## Sobre el proyecto

Este portfolio nació con un doble objetivo: tener un espacio propio donde mostrar mi trabajo en datos, y demostrar de paso que sé construir y desplegar una aplicación web completa. Todo el sitio —frontend, backend, base de datos y despliegue— está hecho a mano.

Los proyectos no están hardcodeados en el HTML: se gestionan dinámicamente desde una base de datos PostgreSQL a través de un panel de administración privado, lo que me permite añadir, editar o eliminar proyectos sin tocar el código.

---

## Características

- **Gestión dinámica de proyectos** — cada proyecto se almacena en base de datos con su descripción, tecnologías, contenido detallado (problema, proceso, resultados), imágenes y enlaces a dashboards.
- **Carrusel de imágenes con lightbox** — galería por proyecto con ampliación de imágenes a pantalla completa.
- **Panel de administración privado** — interfaz protegida para gestionar proyectos, consultar mensajes de contacto y ver analíticas de visitas, con modo claro/oscuro.
- **Analíticas propias** — sistema de tracking de visitas sin cookies de terceros (visitantes únicos, páginas, dispositivos, idiomas).
- **Formulario de contacto** — con notificación por email, confirmación automática al remitente y protección anti-spam (honeypot + rate limiting).
- **Modo claro / oscuro** — con persistencia de preferencia.
- **SEO** — meta tags personalizadas por página, Open Graph, sitemap.xml dinámico y robots.txt.
- **Diseño responsive** — con estética glassmorphism y animaciones de entrada.

---

## Stack técnico

**Backend**
- Python 3.11
- Flask
- SQLAlchemy (ORM)
- PostgreSQL (Supabase)

**Frontend**
- HTML5 / CSS3 (sin frameworks)
- JavaScript vanilla
- Chart.js (gráficos del panel)

**Infraestructura**
- Render (despliegue, con Gunicorn)
- Supabase (base de datos PostgreSQL)
- GitHub (control de versiones)

---

## Proyectos destacados en el sitio

- **EDA · Evolución de Vivienda y Paro en España** — análisis de la relación entre precio de vivienda y desempleo por comunidad autónoma.
- **ML · Predicción de Gravedad en Infracciones de Tráfico** — clasificación binaria con LightGBM para ajuste de primas de seguro.
- **API REST · Predicción de Riesgo** — despliegue del modelo anterior como API con FastAPI.
- **EDA · Steam Store Games** — análisis de 27.000 juegos con dashboard en Looker Studio y Power BI.
- **ML · Detección de Fraude en Tarjetas de Crédito** — clasificación sobre dataset desbalanceado con SMOTE y threshold tuning.

---

## Autor

**Lucas Balaguer Cavalcante** — Analista de Datos
[lucascavalcante.es](https://lucascavalcante.es) · [LinkedIn](https://www.linkedin.com/in/lucasbalaguer/) · [GitHub](https://github.com/LucasBalaguer)