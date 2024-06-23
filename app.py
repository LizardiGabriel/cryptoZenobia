import tkinter as tk
from gui import CondominioApp
from login import LoginWindow
from database_setup import create_database

def open_main_app():
    root = tk.Tk()
    app = CondominioApp(root)
    root.mainloop()

if __name__ == '__main__':
    # Crear la base de datos y las tablas si no existen
    create_database()
    
    # Iniciar la ventana de login
    root = tk.Tk()
    login_window = LoginWindow(root, open_main_app)
    root.mainloop()
