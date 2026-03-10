import os
from flask import Flask, flash, redirect, render_template, request, url_for
from mysql.connector import IntegrityError

from config import Config
from models.citas import actualizar_cita, crear_cita, eliminar_cita, obtener_cita_por_id, obtener_citas_por_documento
from models.pacientes import crear_paciente, obtener_paciente_por_documento
from models.tipos_cita import obtener_tipos_cita


FALLBACK_TIPOS_CITA_CONFIG = {
    "General": {
        "medico": "Dra. Mariana Rojas",
        "direccion_eps": "Cra 15 # 93-47, Bogotá",
        "fecha_disponible": "2026-03-12",
        "hora_disponible": "08:30:00",
    },
    "Odontología": {
        "medico": "Dr. Camilo Torres",
        "direccion_eps": "Av 68 # 21-15, Bogotá",
        "fecha_disponible": "2026-03-13",
        "hora_disponible": "10:00:00",
    },
    "Especialista": {
        "medico": "Dra. Paola Méndez",
        "direccion_eps": "Calle 45 # 19-88, Bogotá",
        "fecha_disponible": "2026-03-14",
        "hora_disponible": "14:30:00",
    },
}


app = Flask(__name__)
app.config.from_object(Config)


def cargar_tipos_cita_config():
    try:
        registros = obtener_tipos_cita()
        if not registros:
            return FALLBACK_TIPOS_CITA_CONFIG

        config = {}
        for fila in registros:
            tipo = fila.get("tipo_cita")
            if not tipo:
                continue
            config[tipo] = {
                "medico": fila.get("medico", ""),
                "direccion_eps": fila.get("direccion_eps", ""),
                "fecha_disponible": str(fila.get("fecha_disponible", "")),
                "hora_disponible": str(fila.get("hora_disponible", "")),
            }

        return config or FALLBACK_TIPOS_CITA_CONFIG
    except Exception:
        return FALLBACK_TIPOS_CITA_CONFIG


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/pacientes/registro", methods=["GET", "POST"])
def registro_paciente():
    if request.method == "POST":
        documento = request.form.get("documento", "").strip()
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        telefono = request.form.get("telefono", "").strip()
        correo = request.form.get("correo", "").strip()
        eps = request.form.get("eps", "").strip()

        if not all([documento, nombre, apellido, telefono, correo, eps]):
            flash("Todos los campos son obligatorios.", "danger")
            return render_template("registro_paciente.html")

        try:
            crear_paciente(documento, nombre, apellido, telefono, correo, eps)
            flash("Paciente registrado correctamente.", "success")
            return redirect(url_for("registro_paciente"))
        except IntegrityError:
            flash("Ya existe un paciente registrado con ese documento.", "warning")
        except Exception:
            flash("No fue posible registrar el paciente.", "danger")

    return render_template("registro_paciente.html")


@app.route("/citas/reserva", methods=["GET", "POST"])
def reservar_cita():
    tipos_config = cargar_tipos_cita_config()
    tipos_cita = list(tipos_config.keys())

    if request.method == "POST":
        documento = request.form.get("documento", "").strip()
        tipo_cita = request.form.get("tipo_cita", "").strip()

        if not all([documento, tipo_cita]):
            flash("Documento y tipo de cita son obligatorios.", "danger")
            return render_template(
                "reservar_cita.html",
                tipos_cita=tipos_cita,
                tipos_config=tipos_config,
            )

        paciente = obtener_paciente_por_documento(documento)
        if not paciente:
            flash("El paciente no existe. Regístralo antes de reservar una cita.", "warning")
            return redirect(url_for("registro_paciente"))

        configuracion = tipos_config.get(tipo_cita)
        if not configuracion:
            flash("No hay configuración disponible para ese tipo de cita.", "danger")
            return render_template(
                "reservar_cita.html",
                tipos_cita=tipos_cita,
                tipos_config=tipos_config,
            )

        try:
            crear_cita(
                documento,
                configuracion["medico"],
                tipo_cita,
                configuracion["fecha_disponible"],
                configuracion["hora_disponible"],
                configuracion["direccion_eps"],
            )
            flash("Cita reservada correctamente con datos autocompletados.", "success")
            return redirect(url_for("consultar_cita"))
        except Exception:
            flash("No fue posible reservar la cita.", "danger")

    return render_template(
        "reservar_cita.html",
        tipos_cita=tipos_cita,
        tipos_config=tipos_config,
    )


@app.route("/citas/consulta", methods=["GET", "POST"])
def consultar_cita():
    citas = None
    documento = ""

    if request.method == "POST":
        documento = request.form.get("documento", "").strip()
        if not documento:
            flash("Debes ingresar un documento.", "warning")
            return render_template("consulta_cita.html", citas=citas, documento=documento)

        citas = obtener_citas_por_documento(documento)
        if not citas:
            flash("No se encontraron citas para el documento ingresado.", "info")

    return render_template("consulta_cita.html", citas=citas, documento=documento)


@app.route("/eps/consulta", methods=["GET", "POST"])
def consultar_eps():
    documento = ""
    paciente = None

    if request.method == "POST":
        documento = request.form.get("documento", "").strip()
        if not documento:
            flash("Debes ingresar un documento.", "warning")
            return render_template("consulta_eps.html", documento=documento, paciente=paciente)

        paciente = obtener_paciente_por_documento(documento)
        if not paciente:
            flash("No se encontró un paciente con ese documento.", "info")

    return render_template("consulta_eps.html", documento=documento, paciente=paciente)


@app.route("/citas/<int:cita_id>/editar", methods=["GET", "POST"])
def editar_cita(cita_id):
    cita = obtener_cita_por_id(cita_id)

    if not cita:
        flash("La cita no existe.", "warning")
        return redirect(url_for("consultar_cita"))

    if request.method == "POST":
        medico = request.form.get("medico", "").strip()
        tipo_cita = request.form.get("tipo_cita", "").strip()
        fecha = request.form.get("fecha", "").strip()
        hora = request.form.get("hora", "").strip()

        if not all([medico, tipo_cita, fecha, hora]):
            flash("Todos los campos son obligatorios para actualizar.", "danger")
            return render_template("resultado_cita.html", cita=cita)

        try:
            actualizado = actualizar_cita(cita_id, medico, tipo_cita, fecha, hora)
            if actualizado:
                flash("Cita actualizada correctamente.", "success")
            else:
                flash("No se realizaron cambios en la cita.", "info")
            return redirect(url_for("consultar_cita"))
        except Exception:
            flash("No fue posible actualizar la cita.", "danger")

    return render_template("resultado_cita.html", cita=cita)


@app.route("/citas/<int:cita_id>/eliminar", methods=["POST"])
def eliminar_cita_route(cita_id):
    try:
        eliminada = eliminar_cita(cita_id)
        if eliminada:
            flash("Cita eliminada correctamente.", "success")
        else:
            flash("No se encontró la cita para eliminar.", "warning")
    except Exception:
        flash("No fue posible eliminar la cita.", "danger")

    return redirect(url_for("consultar_cita"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
