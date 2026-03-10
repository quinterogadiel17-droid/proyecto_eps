import os
import mysql.connector

# Creamos la ruta en una carpeta temporal de Render que siempre tiene permisos
ssl_cert_path = "/tmp/ca.pem"

# Escribimos el contenido de la variable en ese archivo temporal
ca_cert_content = os.getenv('DB_CA_CERT')
if ca_cert_content:
    with open(ssl_cert_path, "w") as f:
        f.write(ca_cert_content)

try:
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=int(os.getenv('DB_PORT', 17382)), # Aiven suele usar 25060
        database=os.getenv('DB_NAME'),
        ssl_ca=ssl_cert_path, # Usamos la ruta temporal
        ssl_verify_cert=True
    )
    print("¡Conectado exitosamente!")
except Exception as e:
    print(f"Error de conexión: {e}")