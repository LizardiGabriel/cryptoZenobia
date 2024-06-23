import tkinter as tk
from tkinter import messagebox
from database_setup import verificar_admin, registrar_admin

class LoginWindow:
    def __init__(self, root, open_main_app):
        self.root = root
        self.root.title("Login Administrador")
        self.open_main_app = open_main_app
        self.create_widgets()

    def create_widgets(self):
        self.label_username = tk.Label(self.root, text="Username")
        self.label_username.pack(pady=10)
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack(pady=10)

        self.label_password = tk.Label(self.root, text="Password")
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack(pady=10)

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self.root, text="Register", command=self.open_register_window)
        self.register_button.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if verificar_admin(username, password):
            self.root.destroy()
            self.open_main_app()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def open_register_window(self):
        RegisterWindow(self.root)

class RegisterWindow:
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Register Administrador")
        self.create_widgets()

    def create_widgets(self):
        self.label_username = tk.Label(self.window, text="Username")
        self.label_username.pack(pady=10)
        self.entry_username = tk.Entry(self.window)
        self.entry_username.pack(pady=10)

        self.label_password = tk.Label(self.window, text="Password")
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(self.window, show="*")
        self.entry_password.pack(pady=10)

        self.register_button = tk.Button(self.window, text="Register", command=self.register)
        self.register_button.pack(pady=10)

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if registrar_admin(username, password):
            messagebox.showinfo("Éxito", "Administrador registrado correctamente")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "El nombre de usuario ya existe")
