import os
import mysql.connector

# Usamos .get() con un valor por defecto para evitar el NoneType
port_env = os.getenv('DB_PORT', 3306) 

connection = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=int(port_env), # Aquí ya no fallará porque port_env siempre tendrá algo
    database=os.getenv('DB_NAME'),
    ssl_ca="ca.pem" # Asegúrate de que el nombre coincida con tu archivo
)