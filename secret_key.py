from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import tkinter as tk
import os
from tkinter import filedialog, messagebox

def create_secret_key():
    try:
        # Seleccionar la clave privada del administrador
        private_key_file = filedialog.askopenfilename(title="Selecciona tu clave privada DH", filetypes=(("PEM files", "*.pem"),))
        if not private_key_file:
            messagebox.showinfo("Cancelado", "Operación cancelada. No se seleccionó ninguna clave privada.")
            return
        
        # Seleccionar la clave pública del auditor
        auditor_public_key_file = filedialog.askopenfilename(title="Selecciona la clave pública DH del auditor", filetypes=(("PEM files", "*.pem"),))
        if not auditor_public_key_file:
            messagebox.showinfo("Cancelado", "Operación cancelada. No se seleccionó ninguna clave pública.")
            return
        
        # Cargar la clave privada del administrador
        with open(private_key_file, 'rb') as key_file:
            private_key = load_pem_private_key(key_file.read(), password=None)
        print("Clave privada del administrador cargada correctamente.")

        # Cargar la clave pública del auditor
        with open(auditor_public_key_file, 'rb') as key_file:
            auditor_public_key = load_pem_public_key(key_file.read())
        print("Clave pública del auditor cargada correctamente.")

        # Generar la clave compartida
        shared_key = private_key.exchange(auditor_public_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data'
        ).derive(shared_key)

        # Guardar la clave derivada en un archivo
        keys_folder = "keys"
        os.makedirs(keys_folder, exist_ok=True)
        derived_key_path = os.path.join(keys_folder, "admin_derived_secret_key.bin")
        
        with open(derived_key_path, 'wb') as key_file:
            key_file.write(derived_key)

        messagebox.showinfo("Éxito", f"Clave secreta derivada guardada en '{derived_key_path}'")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema al generar la clave secreta: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    create_secret_key()
