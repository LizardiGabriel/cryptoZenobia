import tkinter as tk
from gui import CondominioApp
from database_setup import create_database

if __name__ == '__main__':
    # Crear la base de datos y las tablas si no existen
    create_database()
    
    # Inicializar la interfaz gráfica
    root = tk.Tk()
    app = CondominioApp(root)
    root.mainloop()
