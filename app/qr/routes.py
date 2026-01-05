from flask import Blueprint, send_file, render_template, url_for, current_app
from flask_login import login_required
from app.models import Persona, QrToken
from app.extensions import db
import json
import qrcode
from qrcode.constants import ERROR_CORRECT_H
import os
import uuid

qr_bp = Blueprint("qr", __name__, url_prefix="/qr")

# @qr_bp.route("/generar/<int:persona_id>")
# @login_required
# def generar(persona_id):
#     persona = Persona.query.get_or_404(persona_id)

#     qr_token = QrToken(persona_id=persona.id)
#     db.session.add(qr_token)
#     db.session.commit()

#     url = f"http://localhost:5000/qr/ver/{qr_token.token}"

#     img = qrcode.make(url)
#     path = f"app/static/qr/{qr_token.token}.png"
#     img.save(path)

#     return send_file(path, as_attachment=True)


# @qr_bp.route("/generar/<int:persona_id>")
# def generar(persona_id):
#     persona = Persona.query.get_or_404(persona_id)

#     # Crear token si no existe
#     if not persona.qr_token:
#         persona.qr_token = str(uuid.uuid4())
#         db.session.commit()

#     url_publica = url_for(
#         "personas.ver_persona_publica", token=persona.qr_token, _external=True
#     )

#     data = {
#         "nombre": f"{persona.nombres} {persona.apellidos}",
#         "tipo_sangre": persona.tipo_sangre,
#         "contacto": persona.contacto_emergencia,
#         "url": url_publica,
#     }

#     # 📁 Directorio static/qr
#     qr_dir = os.path.join(current_app.root_path, "static", "qr")
#     os.makedirs(qr_dir, exist_ok=True)

#     qr_filename = f"persona_{persona.id}.png"
#     qr_path = os.path.join(qr_dir, qr_filename)

#     #qr = qrcode.make(json.dumps(data))
#     qr = qrcode.make(url_publica)
#     qr.save(qr_path)

#     return render_template(
#         "qr/ver_qr.html",
#         persona=persona,
#         qr_filename=qr_filename,
#         url_publica=url_publica,
#     )


@qr_bp.route("/generar/<int:persona_id>")
def generar(persona_id):
    persona = Persona.query.get_or_404(persona_id)

    # Crear token si no existe
    if not persona.qr_token:
        persona.qr_token = str(uuid.uuid4())
        db.session.commit()

    # URL pública (MANTENER CORTA)
    url_publica = url_for(
        "personas.ver_persona_publica", token=persona.qr_token, _external=True
    )

    # 📁 Directorio static/qr
    qr_dir = os.path.join(current_app.root_path, "static", "qr")
    os.makedirs(qr_dir, exist_ok=True)

    qr_filename = f"persona_{persona.id}.png"
    qr_path = os.path.join(qr_dir, qr_filename)

    # ✅ CONFIGURACIÓN IDEAL PARA TAMAÑO PEQUEÑO
    qr = qrcode.QRCode(
        version=None,  # automático
        error_correction=ERROR_CORRECT_H,  # 🔥 MUY IMPORTANTE
        box_size=12,  # tamaño de cada cuadro
        border=4,  # margen obligatorio
    )

    qr.add_data(url_publica)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Guardar con alta resolución (300 DPI)
    img.save(qr_path, dpi=(300, 300))

    return render_template(
        "qr/ver_qr.html",
        persona=persona,
        qr_filename=qr_filename,
        url_publica=url_publica,
    )


@qr_bp.route("/ver/<uuid:token>")
def ver(token):
    qr = QrToken.query.filter_by(token=token, activo=True).first_or_404()
    persona = qr.persona

    return render_template("qr/ver.html", persona=persona)
