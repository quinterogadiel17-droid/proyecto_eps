from database.conexion import obtener_conexion


def _obtener_tipos_desde_tabla_config(cursor):
    cursor.execute(
        """
        SELECT tipo_cita, medico, direccion_eps, fecha_disponible, hora_disponible
        FROM tipos_cita_config
        ORDER BY tipo_cita ASC
        """
    )
    return cursor.fetchall()


def _obtener_tipos_desde_citas(cursor):
    cursor.execute(
        """
        SELECT
            c.tipo_cita,
            c.medico,
            c.direccion_eps,
            c.fecha AS fecha_disponible,
            c.hora AS hora_disponible
        FROM citas c
        INNER JOIN (
            SELECT tipo_cita, MAX(id) AS max_id
            FROM citas
            GROUP BY tipo_cita
        ) ult ON ult.max_id = c.id
        ORDER BY c.tipo_cita ASC
        """
    )
    return cursor.fetchall()


def obtener_tipos_cita():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        try:
            registros = _obtener_tipos_desde_tabla_config(cursor)
            if registros:
                return registros
        except Exception:
            pass

        return _obtener_tipos_desde_citas(cursor)
    finally:
        cursor.close()
        conexion.close()


def obtener_configuracion_tipo(tipo_cita):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        try:
            cursor.execute(
                """
                SELECT tipo_cita, medico, direccion_eps, fecha_disponible, hora_disponible
                FROM tipos_cita_config
                WHERE tipo_cita = %s
                """,
                (tipo_cita,),
            )
            registro = cursor.fetchone()
            if registro:
                return registro
        except Exception:
            pass

        cursor.execute(
            """
            SELECT
                tipo_cita,
                medico,
                direccion_eps,
                fecha AS fecha_disponible,
                hora AS hora_disponible
            FROM citas
            WHERE tipo_cita = %s
            ORDER BY id DESC
            LIMIT 1
            """,
            (tipo_cita,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conexion.close()
