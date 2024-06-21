import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding, dh
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# Generar y almacenar clave AES usando PBKDF2HMAC
def generar_clave_aes(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(password.encode())

# Cifrar datos usando AES
def cifrar_datos(datos: bytes, clave: bytes) -> bytes:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(clave), modes.CFB(iv))
    encryptor = cipher.encryptor()
    datos_cifrados = encryptor.update(datos) + encryptor.finalize()
    return iv + datos_cifrados

# Descrifrar datos usando AES
def descifrar_datos(datos_cifrados: bytes, clave: bytes) -> bytes:
    iv = datos_cifrados[:16]
    datos_cifrados = datos_cifrados[16:]
    cipher = Cipher(algorithms.AES(clave), modes.CFB(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(datos_cifrados) + decryptor.finalize()

# Generar claves Diffie-Hellman
def generar_claves_diffie_hellman():
    parameters = dh.generate_parameters(generator=2, key_size=2048)
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

# Generar clave compartida usando Diffie-Hellman
def generar_clave_compartida(private_key, peer_public_key_bytes):
    peer_public_key = dh.DHPublicKey.from_public_bytes(peer_public_key_bytes)
    shared_key = private_key.exchange(peer_public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data'
    ).derive(shared_key)
    return derived_key

# Clase para manejar firmas y verificaciones usando RSA
class RSAUtils:
    def __init__(self, private_key_path=None):
        if private_key_path:
            with open(private_key_path, "rb") as key_file:
                self.private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None
                )
            self.public_key = self.private_key.public_key()
        else:
            self.private_key = None
            self.public_key = None

    def cargar_clave_privada(self, private_key_path):
        with open(private_key_path, "rb") as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
        self.public_key = self.private_key.public_key()

    def firmar_documento(self, datos: bytes) -> bytes:
        if self.private_key is None:
            raise ValueError("Private key not loaded.")
        return self.private_key.sign(
            datos,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    def verificar_firma(self, datos: bytes, firma: bytes):
        if self.public_key is None:
            raise ValueError("Public key not available.")
        self.public_key.verify(
            firma,
            datos,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    def exportar_clave_publica(self) -> bytes:
        if self.public_key is None:
            raise ValueError("Public key not available.")
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

# Generar hash usando SHA-256
def generar_hash(datos: bytes) -> bytes:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(datos)
    return digest.finalize()
