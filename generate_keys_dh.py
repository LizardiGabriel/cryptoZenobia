from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
import os
import tkinter.messagebox as messagebox

def create_dh_parameters():
    parameters = dh.generate_parameters(generator=2, key_size=2048)
    keys_folder = "keys"
    os.makedirs(keys_folder, exist_ok=True)
    with open(os.path.join(keys_folder, "dh_parameters.pem"), "wb") as param_file:
        param_file.write(parameters.parameter_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.ParameterFormat.PKCS3
        ))
    return parameters

def create_dh_keys():
    try:
        parameters = create_dh_parameters()

        private_key = parameters.generate_private_key()
        public_key = private_key.public_key()

        keys_folder = "keys"
        os.makedirs(keys_folder, exist_ok=True)

        with open(os.path.join(keys_folder, "dh_private_key_administrador.pem"), "wb") as private_file:
            private_file.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

        with open(os.path.join(keys_folder, "dh_public_key_administrador.pem"), "wb") as public_file:
            public_file.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )

        messagebox.showinfo("Éxito", "Las claves DH y los parámetros se crearon y guardaron correctamente en la carpeta 'keys'.")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema al crear las claves DH: {e}")

if __name__ == "__main__":
    create_dh_keys()
