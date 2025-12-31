from .extensions import db
from flask_login import UserMixin
from datetime import datetime
import uuid


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)


class Persona(db.Model):
    __tablename__ = "personas"

    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(10), unique=True, nullable=False)
    nombres = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    tipo_sangre = db.Column(db.String(5))
    alergias = db.Column(db.Text)
    enfermedades = db.Column(db.Text)
    medicamentos = db.Column(db.Text)
    contacto_emergencia = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    qr_token = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))


class QrToken(db.Model):
    __tablename__ = "qr_tokens"

    id = db.Column(db.Integer, primary_key=True)
    persona_id = db.Column(db.Integer, db.ForeignKey("personas.id"))
    token = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    persona = db.relationship("Persona")
