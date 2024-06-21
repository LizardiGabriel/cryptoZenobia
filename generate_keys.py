from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os
import sqlite3

# Generar un par de claves RSA de 2048 bits
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# Convertir las claves en formato PEM para poder guardarlas en un archivo
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Guardar la clave privada en un archivo
private_key_file = "private_key.pem"
with open(private_key_file, "wb") as f:
    f.write(private_pem)

print(f"Clave privada guardada en: {private_key_file}")

# Guardar la clave pública en la base de datos
def store_public_key(public_pem):
    conn = sqlite3.connect('condominio.db')
    c = conn.cursor()

    # Crear la tabla para almacenar la clave pública si no existe
    c.execute('''
        CREATE TABLE IF NOT EXISTS public_key (
            id INTEGER PRIMARY KEY,
            key TEXT NOT NULL
        )
    ''')

    # Insertar la clave pública
    c.execute('DELETE FROM public_key')  # Eliminar cualquier clave pública existente
    c.execute('INSERT INTO public_key (key) VALUES (?)', (public_pem.decode('utf-8'),))

    conn.commit()
    conn.close()

store_public_key(public_pem)
print("Clave pública guardada en la base de datos.")
