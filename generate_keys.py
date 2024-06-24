from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

def generate_keys():
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

    # Definir la carpeta para guardar las claves
    keys_folder = "keys"
    os.makedirs(keys_folder, exist_ok=True)

    # Guardar la clave privada en un archivo
    private_key_file = os.path.join(keys_folder, "private_key.pem")
    with open(private_key_file, "wb") as f:
        f.write(private_pem)

    print(f"Clave privada guardada en: {private_key_file}")

    # Guardar la clave pública en un archivo
    public_key_file = os.path.join(keys_folder, "public_key.pem")
    with open(public_key_file, "wb") as f:
        f.write(public_pem)

    print(f"Clave pública guardada en: {public_key_file}")

if __name__ == "__main__":
    generate_keys()
