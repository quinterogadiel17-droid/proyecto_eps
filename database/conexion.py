import os
import mysql.connector

# Si guardaste el certificado en el root de tu proyecto
connection = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    ssl_ca="ca.pem", # Archivo del certificado de Aiven
    ssl_verify_cert=True
)
