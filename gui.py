import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sqlite3
from database_setup import agregar_inquilino, eliminar_inquilino, registrar_pago_mantenimiento, registrar_pago_proveedor, obtener_inquilinos, obtener_pagos_mantenimiento, obtener_pagos_proveedores, obtener_pagos_por_inquilino, obtener_monto_pago_actual
from document_generator import generar_cupon_pago, generar_certificado_estado
from crypto_utils import RSAUtils

class CondominioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Administrador de Condominios")
        self.create_widgets()
        self.load_inquilinos()
        self.load_pagos()
        self.load_proveedores()
        self.rsa_utils = RSAUtils()

    def create_widgets(self):
        tab_control = ttk.Notebook(self.root)

        # Tab for Inquilinos
        self.inquilinos_tab = ttk.Frame(tab_control)
        tab_control.add(self.inquilinos_tab, text='Inquilinos')

        self.inquilinos_list = ttk.Treeview(self.inquilinos_tab, columns=('ID', 'Nombre Completo'), show='headings')
        self.inquilinos_list.heading('ID', text='ID')
        self.inquilinos_list.heading('Nombre Completo', text='Nombre Completo')
        self.inquilinos_list.pack(expand=True, fill=tk.BOTH)

        self.add_inquilino_button = tk.Button(self.inquilinos_tab, text="Agregar Inquilino", command=self.add_inquilino)
        self.add_inquilino_button.pack(pady=10)

        self.del_inquilino_button = tk.Button(self.inquilinos_tab, text="Eliminar Inquilino", command=self.del_inquilino)
        self.del_inquilino_button.pack(pady=10)

        self.gen_cupon_button = tk.Button(self.inquilinos_tab, text="Generar Cupon de Pago", command=self.gen_cupon)
        self.gen_cupon_button.pack(pady=10)

        self.gen_cert_button = tk.Button(self.inquilinos_tab, text="Generar Certificado de Estado", command=self.gen_certificado)
        self.gen_cert_button.pack(pady=10)

        self.sign_doc_button = tk.Button(self.inquilinos_tab, text="Firmar Documento", command=self.sign_document)
        self.sign_doc_button.pack(pady=10)

        # Tab for Pagos de Mantenimiento
        self.pagos_tab = ttk.Frame(tab_control)
        tab_control.add(self.pagos_tab, text='Pagos de Mantenimiento')

        self.pagos_list = ttk.Treeview(self.pagos_tab, columns=('ID', 'Inquilino', 'Mes', 'Monto'), show='headings')
        self.pagos_list.heading('ID', text='ID')
        self.pagos_list.heading('Inquilino', text='Inquilino')
        self.pagos_list.heading('Mes', text='Mes')
        self.pagos_list.heading('Monto', text='Monto')
        self.pagos_list.pack(expand=True, fill=tk.BOTH)

        self.add_pago_button = tk.Button(self.pagos_tab, text="Registrar Pago", command=self.add_pago)
        self.add_pago_button.pack(pady=10)

        # Tab for Pagos a Proveedores
        self.proveedores_tab = ttk.Frame(tab_control)
        tab_control.add(self.proveedores_tab, text='Pagos a Proveedores')

        self.proveedores_list = ttk.Treeview(self.proveedores_tab, columns=('ID', 'Proveedor', 'Fecha', 'Monto'), show='headings')
        self.proveedores_list.heading('ID', text='ID')
        self.proveedores_list.heading('Proveedor', text='Proveedor')
        self.proveedores_list.heading('Fecha', text='Fecha')
        self.proveedores_list.heading('Monto', text='Monto')
        self.proveedores_list.pack(expand=True, fill=tk.BOTH)

        self.add_proveedor_button = tk.Button(self.proveedores_tab, text="Registrar Pago a Proveedor", command=self.add_proveedor)
        self.add_proveedor_button.pack(pady=10)

        tab_control.pack(expand=True, fill=tk.BOTH)

    def add_inquilino(self):
        # Ventana para agregar un nuevo inquilino
        def save_inquilino():
            nombre_completo = entry_nombre.get()
            if nombre_completo:
                agregar_inquilino(nombre_completo)
                messagebox.showinfo("Éxito", "Inquilino agregado correctamente")
                win_add_inquilino.destroy()
                self.load_inquilinos()
            else:
                messagebox.showwarning("Error", "El nombre no puede estar vacío")

        win_add_inquilino = tk.Toplevel(self.root)
        win_add_inquilino.title("Agregar Inquilino")

        label_nombre = tk.Label(win_add_inquilino, text="Nombre Completo")
        label_nombre.pack(pady=10)
        entry_nombre = tk.Entry(win_add_inquilino)
        entry_nombre.pack(pady=10)

        btn_save = tk.Button(win_add_inquilino, text="Guardar", command=save_inquilino)
        btn_save.pack(pady=10)

    def del_inquilino(self):
        # Función para eliminar un inquilino seleccionado
        selected_item = self.inquilinos_list.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Debe seleccionar un inquilino para eliminar")
            return

        inquilino_id = self.inquilinos_list.item(selected_item[0])['values'][0]
        eliminar_inquilino(inquilino_id)
        messagebox.showinfo("Éxito", "Inquilino eliminado correctamente")
        self.load_inquilinos()

    def add_pago(self):
        # Ventana para agregar un nuevo pago de mantenimiento
        def save_pago():
            inquilino_id = inquilinos_combobox.get().split()[0]
            mes = entry_mes.get()
            monto = entry_monto.get()
            if inquilino_id and mes and monto:
                registrar_pago_mantenimiento(inquilino_id, mes, float(monto))
                messagebox.showinfo("Éxito", "Pago registrado correctamente")
                win_add_pago.destroy()
                self.load_pagos()
            else:
                messagebox.showwarning("Error", "Todos los campos son obligatorios")

        win_add_pago = tk.Toplevel(self.root)
        win_add_pago.title("Registrar Pago")

        inquilinos = obtener_inquilinos()

        label_inquilino = tk.Label(win_add_pago, text="Inquilino")
        label_inquilino.pack(pady=10)
        inquilinos_combobox = ttk.Combobox(win_add_pago, values=[f"{i['id']} - {i['nombre_completo']}" for i in inquilinos])
        inquilinos_combobox.pack(pady=10)

        label_mes = tk.Label(win_add_pago, text="Mes")
        label_mes.pack(pady=10)
        entry_mes = tk.Entry(win_add_pago)
        entry_mes.pack(pady=10)

        label_monto = tk.Label(win_add_pago, text="Monto")
        label_monto.pack(pady=10)
        entry_monto = tk.Entry(win_add_pago)
        entry_monto.pack(pady=10)

        btn_save = tk.Button(win_add_pago, text="Guardar", command=save_pago)
        btn_save.pack(pady=10)

    def add_proveedor(self):
        # Ventana para agregar un nuevo pago a proveedor
        def save_proveedor():
            proveedor = entry_proveedor.get()
            fecha = entry_fecha.get()
            monto = entry_monto.get()
            if proveedor and fecha and monto:
                registrar_pago_proveedor(proveedor, fecha, float(monto))
                messagebox.showinfo("Éxito", "Pago a proveedor registrado correctamente")
                win_add_proveedor.destroy()
                self.load_proveedores()
            else:
                messagebox.showwarning("Error", "Todos los campos son obligatorios")

        win_add_proveedor = tk.Toplevel(self.root)
        win_add_proveedor.title("Registrar Pago a Proveedor")

        label_proveedor = tk.Label(win_add_proveedor, text="Proveedor")
        label_proveedor.pack(pady=10)
        entry_proveedor = tk.Entry(win_add_proveedor)
        entry_proveedor.pack(pady=10)

        label_fecha = tk.Label(win_add_proveedor, text="Fecha")
        label_fecha.pack(pady=10)
        entry_fecha = tk.Entry(win_add_proveedor)
        entry_fecha.pack(pady=10)

        label_monto = tk.Label(win_add_proveedor, text="Monto")
        label_monto.pack(pady=10)
        entry_monto = tk.Entry(win_add_proveedor)
        entry_monto.pack(pady=10)

        btn_save = tk.Button(win_add_proveedor, text="Guardar", command=save_proveedor)
        btn_save.pack(pady=10)

    def gen_cupon(self):
        # Función para generar cupón de pago para el inquilino seleccionado
        selected_item = self.inquilinos_list.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Debe seleccionar un inquilino para generar el cupón de pago")
            return

        inquilino_id = self.inquilinos_list.item(selected_item[0])['values'][0]
        inquilino_nombre = self.inquilinos_list.item(selected_item[0])['values'][1]

        mes = "Junio"  # Se puede cambiar para obtener el mes actual o especificar otro mes
        monto = obtener_monto_pago_actual(inquilino_id, mes)  # Obtener el monto real del pago desde la base de datos
        if monto is None:
            messagebox.showwarning("Error", f"No se encontró un pago para el inquilino {inquilino_nombre} en el mes de {mes}")
            return
        ruta_archivo = f"cupon_{inquilino_nombre}_{mes}.pdf"

        inquilino = {'id': inquilino_id, 'nombre_completo': inquilino_nombre}
        generar_cupon_pago(inquilino, mes, monto, ruta_archivo)

        messagebox.showinfo("Éxito", f"Cupon de pago generado: {ruta_archivo}")

    def gen_certificado(self):
        # Función para generar certificado de estado para el inquilino seleccionado
        selected_item = self.inquilinos_list.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Debe seleccionar un inquilino para generar el certificado de estado")
            return

        inquilino_id = self.inquilinos_list.item(selected_item[0])['values'][0]
        inquilino_nombre = self.inquilinos_list.item(selected_item[0])['values'][1]

        ruta_archivo = f"certificado_estado_{inquilino_nombre}.pdf"

        inquilino = {'id': inquilino_id, 'nombre_completo': inquilino_nombre}
        pagos = obtener_pagos_por_inquilino(inquilino_id)
        generar_certificado_estado(inquilino, pagos, ruta_archivo)

        messagebox.showinfo("Éxito", f"Certificado de estado generado: {ruta_archivo}")

    def sign_document(self):
        # Función para cargar clave privada y firmar documento
        private_key_path = filedialog.askopenfilename(title="Seleccionar clave privada", filetypes=(("PEM files", "*.pem"), ("All files", "*.*")))
        document_path = filedialog.askopenfilename(title="Seleccionar documento a firmar", filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")))

        if private_key_path and document_path:
            try:
                self.rsa_utils.cargar_clave_privada(private_key_path)
                with open(document_path, "rb") as doc:
                    document_data = doc.read()
                    signature = self.rsa_utils.firmar_documento(document_data)

                # Guardar la firma en la base de datos
                self.guardar_documento_firmado(document_path, signature)

                messagebox.showinfo("Éxito", "Documento firmado y guardado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al firmar el documento: {str(e)}")

    def guardar_documento_firmado(self, document_path, signature):
        with open(document_path, "rb") as doc:
            document_data = doc.read()

        conn = sqlite3.connect('condominio.db')
        c = conn.cursor()
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS documentos_firmados (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                documento BLOB NOT NULL,
                firma BLOB NOT NULL
            )
        ''')

        nombre = os.path.basename(document_path)
        c.execute('INSERT INTO documentos_firmados (nombre, documento, firma) VALUES (?, ?, ?)',
                  (nombre, document_data, signature))
        
        conn.commit()
        conn.close()

    def load_inquilinos(self):
        # Cargar la lista de inquilinos desde la base de datos
        for row in self.inquilinos_list.get_children():
            self.inquilinos_list.delete(row)
        inquilinos = obtener_inquilinos()
        for inquilino in inquilinos:
            self.inquilinos_list.insert('', 'end', values=(inquilino['id'], inquilino['nombre_completo']))

    def load_pagos(self):
        # Cargar la lista de pagos de mantenimiento desde la base de datos
        for row in self.pagos_list.get_children():
            self.pagos_list.delete(row)
        pagos = obtener_pagos_mantenimiento()
        for pago in pagos:
            self.pagos_list.insert('', 'end', values=(pago['id'], pago['nombre_completo'], pago['mes'], pago['monto']))

    def load_proveedores(self):
        # Cargar la lista de pagos a proveedores desde la base de datos
        for row in self.proveedores_list.get_children():
            self.proveedores_list.delete(row)
        proveedores = obtener_pagos_proveedores()
        for proveedor in proveedores:
            self.proveedores_list.insert('', 'end', values=(proveedor['id'], proveedor['proveedor'], proveedor['fecha'], proveedor['monto']))
