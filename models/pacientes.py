from database.conexion import obtener_conexion


def crear_paciente(documento, nombre, apellido, telefono, correo, eps):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            INSERT INTO pacientes (documento, nombre, apellido, telefono, correo, eps)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (documento, nombre, apellido, telefono, correo, eps),
        )
        conexion.commit()
        return True
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


def obtener_paciente_por_documento(documento):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT id, documento, nombre, apellido, telefono, correo, eps
            FROM pacientes
            WHERE documento = %s
            """,
            (documento,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conexion.close()
