from database.conexion import obtener_conexion


def crear_cita(documento, medico, tipo_cita, fecha, hora, direccion_eps):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            INSERT INTO citas (documento, medico, tipo_cita, fecha, hora, direccion_eps)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (documento, medico, tipo_cita, fecha, hora, direccion_eps),
        )
        conexion.commit()
        return cursor.lastrowid
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


def obtener_citas_por_documento(documento):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT
                c.id,
                p.documento,
                p.nombre,
                p.apellido,
                p.eps AS eps_registrada,
                c.medico,
                c.tipo_cita,
                c.fecha,
                c.hora,
                c.direccion_eps
            FROM citas c
            INNER JOIN pacientes p ON p.documento = c.documento
            WHERE c.documento = %s
            ORDER BY c.fecha DESC, c.hora DESC
            """,
            (documento,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()


def obtener_cita_por_id(cita_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT id, documento, medico, tipo_cita, fecha, hora, direccion_eps
            FROM citas
            WHERE id = %s
            """,
            (cita_id,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conexion.close()


def actualizar_cita(cita_id, medico, tipo_cita, fecha, hora):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            UPDATE citas
            SET medico = %s, tipo_cita = %s, fecha = %s, hora = %s
            WHERE id = %s
            """,
            (medico, tipo_cita, fecha, hora, cita_id),
        )
        conexion.commit()
        return cursor.rowcount > 0
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


def eliminar_cita(cita_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM citas WHERE id = %s", (cita_id,))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()
