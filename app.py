import os
import hashlib
from functools import wraps
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
from flask import (
    Flask, render_template, session, redirect,
    url_for, request, flash, abort
)

load_dotenv()

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# ----------------------------
# CONFIGURACIÓN BASE DE DATOS
# En local → SQLite | En producción → Supabase (PostgreSQL)
# ----------------------------

db_url = os.getenv("DATABASE_URL", "sqlite:///projects.db")

# Supabase devuelve "postgres://", SQLAlchemy necesita "postgresql://"
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Evita timeouts en conexiones PostgreSQL de larga duración
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}

db = SQLAlchemy(app)


# ----------------------------
# MODELOS
# ----------------------------

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(150))
    tech = db.Column(db.String(300))
    duration = db.Column(db.String(100))
    github = db.Column(db.String(300))

    def __repr__(self):
        return f"<Project {self.title}>"


class PageVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(200), nullable=False)
    ip_hash = db.Column(db.String(64), nullable=False)
    language = db.Column(db.String(50))
    device = db.Column(db.String(20))
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)
    visit_date = db.Column(db.Date, default=date.today)

    def __repr__(self):
        return f"<PageVisit {self.page} {self.visit_date}>"


# ----------------------------
# DECORADORES
# ----------------------------

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function


def panel_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("panel"):
            token = request.view_args.get("token", "")
            return redirect(url_for("panel_login", token=token))
        return f(*args, **kwargs)
    return decorated_function


# ----------------------------
# TRACKING DE VISITAS
# ----------------------------

def _hash_ip(ip: str) -> str:
    return hashlib.sha256(ip.encode()).hexdigest()


def _detect_device(ua: str) -> str:
    ua = ua.lower()
    if any(k in ua for k in ("mobile", "android", "iphone", "ipad")):
        return "mobile"
    return "desktop"


def track_visit(page: str):
    try:
        ip = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown")
        ip = ip.split(",")[0].strip()
        ip_hash = _hash_ip(ip)
        today = date.today()

        already = PageVisit.query.filter_by(
            ip_hash=ip_hash,
            page=page,
            visit_date=today
        ).first()

        if not already:
            ua = request.headers.get("User-Agent", "")
            lang = request.headers.get("Accept-Language", "")[:50]
            device = _detect_device(ua)
            db.session.add(PageVisit(
                page=page,
                ip_hash=ip_hash,
                language=lang,
                device=device,
                visit_date=today,
            ))
            db.session.commit()
    except Exception:
        db.session.rollback()


# ----------------------------
# RUTAS PÚBLICAS
# ----------------------------

@app.route("/")
def home():
    track_visit("home")
    return render_template("index.html")


@app.route("/proyectos")
def projects():
    track_visit("proyectos")
    all_projects = Project.query.all()
    return render_template("proyectos.html", projects=all_projects)


@app.route("/projects/<slug>")
def project_detail(slug):
    project = Project.query.filter_by(slug=slug).first_or_404()
    track_visit(f"project:{slug}")

    all_projects = Project.query.all()
    ids = [p.id for p in all_projects]
    idx = ids.index(project.id)
    prev_project = all_projects[idx - 1] if idx > 0 else None
    next_project = all_projects[idx + 1] if idx < len(all_projects) - 1 else None

    return render_template(
        "project_detail.html",
        project=project,
        prev_project=prev_project,
        next_project=next_project
    )


@app.route("/skills")
def skills():
    track_visit("skills")
    return render_template("skills.html")


@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    track_visit("contacto")
    success = False
    if request.method == "POST":
        success = True
    return render_template("contact.html", success=success)


# ----------------------------
# RUTAS ADMIN
# ----------------------------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("password") == os.getenv("ADMIN_PASSWORD"):
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))


@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    return render_template("admin_dashboard.html", projects=Project.query.all())


@app.route("/admin/project/new", methods=["GET", "POST"])
@admin_required
def admin_create_project():
    if request.method == "POST":
        db.session.add(Project(
            title=request.form.get("title"),
            description=request.form.get("description"),
            slug=request.form.get("slug"),
            role=request.form.get("role"),
            tech=request.form.get("tech"),
            duration=request.form.get("duration"),
            github=request.form.get("github")
        ))
        db.session.commit()
        flash("Proyecto creado correctamente")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin_project_form.html", action="Crear")


@app.route("/admin/project/<int:id>/edit", methods=["GET", "POST"])
@admin_required
def admin_edit_project(id):
    project = Project.query.get_or_404(id)
    if request.method == "POST":
        project.title = request.form.get("title")
        project.description = request.form.get("description")
        project.slug = request.form.get("slug")
        project.role = request.form.get("role")
        project.tech = request.form.get("tech")
        project.duration = request.form.get("duration")
        project.github = request.form.get("github")
        db.session.commit()
        flash("Proyecto actualizado correctamente")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin_project_form.html", project=project, action="Editar")


@app.route("/admin/project/<int:id>/delete", methods=["POST"])
@admin_required
def admin_delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash("Proyecto eliminado correctamente")
    return redirect(url_for("admin_dashboard"))


# ============================================================
# PANEL PRIVADO
# ============================================================

PANEL_TOKEN = os.getenv("PANEL_TOKEN")
PANEL_PASSWORD = os.getenv("PANEL_PASSWORD")


def _validate_token(token: str) -> bool:
    return bool(token and token == PANEL_TOKEN)


@app.route("/panel/<token>/login", methods=["GET", "POST"])
def panel_login(token):
    if not _validate_token(token):
        abort(404)
    if request.method == "POST":
        if request.form.get("password") == PANEL_PASSWORD:
            session["panel"] = True
            session["panel_token"] = token
            return redirect(url_for("panel_dashboard", token=token))
        flash("Contraseña incorrecta")
    return render_template("panel_login.html", token=token)


@app.route("/panel/<token>/logout")
def panel_logout(token):
    session.pop("panel", None)
    session.pop("panel_token", None)
    return redirect(url_for("panel_login", token=token))


@app.route("/panel/<token>/")
@panel_required
def panel_dashboard(token):
    if not _validate_token(token):
        abort(404)

    from sqlalchemy import func

    today = date.today()
    last_30 = today - timedelta(days=30)

    total_unique = db.session.query(PageVisit.ip_hash).distinct().count()
    unique_30d = db.session.query(PageVisit.ip_hash).filter(
        PageVisit.visit_date >= last_30
    ).distinct().count()

    visits_by_page = db.session.query(
        PageVisit.page,
        func.count(PageVisit.ip_hash.distinct()).label("unique_visitors")
    ).filter(PageVisit.visit_date >= last_30).group_by(PageVisit.page).order_by(
        func.count(PageVisit.ip_hash.distinct()).desc()
    ).all()

    top_languages = db.session.query(
        PageVisit.language,
        func.count().label("total")
    ).filter(PageVisit.visit_date >= last_30).group_by(
        PageVisit.language
    ).order_by(func.count().desc()).limit(5).all()

    devices = db.session.query(
        PageVisit.device,
        func.count().label("total")
    ).filter(PageVisit.visit_date >= last_30).group_by(PageVisit.device).all()

    daily_visits = db.session.query(
        PageVisit.visit_date,
        func.count(PageVisit.ip_hash.distinct()).label("unique_visitors")
    ).filter(
        PageVisit.visit_date >= today - timedelta(days=13)
    ).group_by(PageVisit.visit_date).order_by(PageVisit.visit_date).all()

    return render_template(
        "panel_dashboard.html",
        token=token,
        total_unique=total_unique,
        unique_30d=unique_30d,
        visits_by_page=visits_by_page,
        top_languages=top_languages,
        devices=devices,
        daily_visits=daily_visits,
        projects=Project.query.all(),
    )


@app.route("/panel/<token>/project/new", methods=["GET", "POST"])
@panel_required
def panel_create_project(token):
    if not _validate_token(token):
        abort(404)
    if request.method == "POST":
        db.session.add(Project(
            title=request.form.get("title"),
            description=request.form.get("description"),
            slug=request.form.get("slug"),
            role=request.form.get("role"),
            tech=request.form.get("tech"),
            duration=request.form.get("duration"),
            github=request.form.get("github")
        ))
        db.session.commit()
        flash("Proyecto creado correctamente")
        return redirect(url_for("panel_dashboard", token=token))
    return render_template("panel_project_form.html", token=token, action="Crear", project=None)


@app.route("/panel/<token>/project/<int:id>/edit", methods=["GET", "POST"])
@panel_required
def panel_edit_project(token, id):
    if not _validate_token(token):
        abort(404)
    project = Project.query.get_or_404(id)
    if request.method == "POST":
        project.title = request.form.get("title")
        project.description = request.form.get("description")
        project.slug = request.form.get("slug")
        project.role = request.form.get("role")
        project.tech = request.form.get("tech")
        project.duration = request.form.get("duration")
        project.github = request.form.get("github")
        db.session.commit()
        flash("Proyecto actualizado correctamente")
        return redirect(url_for("panel_dashboard", token=token))
    return render_template("panel_project_form.html", token=token, action="Editar", project=project)


@app.route("/panel/<token>/project/<int:id>/delete", methods=["POST"])
@panel_required
def panel_delete_project(token, id):
    if not _validate_token(token):
        abort(404)
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash("Proyecto eliminado")
    return redirect(url_for("panel_dashboard", token=token))


# ----------------------------
# CREAR TABLAS
# ----------------------------

with app.app_context():
    db.create_all()


# ----------------------------
# RUN
# ----------------------------

if __name__ == "__main__":
    app.run(debug=True)
