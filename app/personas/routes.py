from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Persona
from app.extensions import db

personas_bp = Blueprint("personas", __name__, url_prefix="/personas")


@personas_bp.route("/")
@login_required
def listar():
    personas = Persona.query.all()
    return render_template("personas/listar.html", personas=personas)


@personas_bp.route("/crear", methods=["POST"])
@login_required
def crear():
    if Persona.query.filter_by(cedula=request.form["cedula"]).first():
        flash("La cédula ya está registrada")
        return redirect(url_for("personas.listar"))

    persona = Persona(
        cedula=request.form["cedula"],
        nombres=request.form["nombres"],
        apellidos=request.form["apellidos"],
    )
    db.session.add(persona)
    db.session.commit()

    return redirect(url_for("personas.listar"))


@personas_bp.route("/publico/<token>")
def ver_persona_publica(token):
    persona = Persona.query.filter_by(qr_token=token).first_or_404()
    return render_template("personas/publico.html", persona=persona)


@personas_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    persona = Persona.query.get_or_404(id)

    print(persona.id, persona.nombres)

    if request.method == "POST":
        persona.nombres = request.form["nombres"]
        persona.apellidos = request.form["apellidos"]
        persona.tipo_sangre = request.form["tipo_sangre"]
        persona.alergias = request.form["alergias"]
        persona.enfermedades = request.form["enfermedades"]
        persona.medicamentos = request.form["medicamentos"]
        persona.contacto_emergencia = request.form["contacto_emergencia"]
        persona.observaciones = request.form["observaciones"]
        db.session.commit()

        flash("Persona actualizada correctamente", "success")

        return redirect(url_for("personas.listar"))

    return render_template("personas/editar.html", persona=persona)
