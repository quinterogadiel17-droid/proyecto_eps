import mysql.connector
import os # Importante para que funcione en internet

def obtener_conexion():
    return mysql.connector.connect(
        # Aquí ponemos los datos que te dio Aiven
        host=os.getenv('DB_HOST', 'localhost'), 
        port=os.getenv('DB_PORT', 3306),
        user=os.getenv('DB_USER', 'root'), 
        password=os.getenv('DB_PASSWORD', ''), 
        database=os.getenv('DB_NAME', 'eps_citas')
    
    )
    

