import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from database_setup import agregar_inquilino, eliminar_inquilino, registrar_pago_mantenimiento, registrar_pago_proveedor, obtener_inquilinos, obtener_pagos_mantenimiento, obtener_pagos_proveedores, obtener_pagos_por_inquilino, obtener_monto_pago_actual, guardar_documento_firmado
from document_generator import generar_cupon_pago, generar_certificado_estado
from crypto_utils import RSAUtils

class CondominioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Administrador de Condominios")
        self.create_menu()
        self.rsa_utils = RSAUtils()

    def create_menu(self):
        # Crear el frame para el menú
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Crear botones del menú
        btn_inquilinos = tk.Button(menu_frame, text="Inquilinos", command=self.show_inquilinos)
        btn_inquilinos.pack(fill=tk.X, pady=5)

        btn_pagos_mantenimiento = tk.Button(menu_frame, text="Pago de Mantenimiento", command=self.show_pagos_mantenimiento)
        btn_pagos_mantenimiento.pack(fill=tk.X, pady=5)

        btn_pagos_proveedores = tk.Button(menu_frame, text="Pago a Proveedores", command=self.show_pagos_proveedores)
        btn_pagos_proveedores.pack(fill=tk.X, pady=5)

        btn_gen_cupon = tk.Button(menu_frame, text="Generar Cupon de Pago", command=self.gen_cupon)
        btn_gen_cupon.pack(fill=tk.X, pady=5)

        btn_gen_certificado = tk.Button(menu_frame, text="Generar Certificado de Estado", command=self.gen_certificado)
        btn_gen_certificado.pack(fill=tk.X, pady=5)

        btn_sign_doc = tk.Button(menu_frame, text="Firmar Documento", command=self.sign_document)
        btn_sign_doc.pack(fill=tk.X, pady=5)

    def show_inquilinos(self):
        # Ventana para mostrar y gestionar inquilinos
        def load_inquilinos():
            for row in self.inquilinos_list.get_children():
                self.inquilinos_list.delete(row)
            inquilinos = obtener_inquilinos()
            for inquilino in inquilinos:
                self.inquilinos_list.insert('', 'end', values=(inquilino['id'], inquilino['nombre_completo']))

        def add_inquilino():
            # Ventana para agregar un nuevo inquilino
            def save_inquilino():
                nombre_completo = entry_nombre.get()
                if nombre_completo:
                    agregar_inquilino(nombre_completo)
                    messagebox.showinfo("Éxito", "Inquilino agregado correctamente")
                    win_add_inquilino.destroy()
                    load_inquilinos()
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

        def del_inquilino():
            # Función para eliminar un inquilino seleccionado
            selected_item = self.inquilinos_list.selection()
            if not selected_item:
                messagebox.showwarning("Error", "Debe seleccionar un inquilino para eliminar")
                return

            inquilino_id = self.inquilinos_list.item(selected_item[0])['values'][0]
            eliminar_inquilino(inquilino_id)
            messagebox.showinfo("Éxito", "Inquilino eliminado correctamente")
            load_inquilinos()

        win_inquilinos = tk.Toplevel(self.root)
        win_inquilinos.title("Gestión de Inquilinos")

        self.inquilinos_list = ttk.Treeview(win_inquilinos, columns=('ID', 'Nombre Completo'), show='headings')
        self.inquilinos_list.heading('ID', text='ID')
        self.inquilinos_list.heading('Nombre Completo', text='Nombre Completo')
        self.inquilinos_list.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        btn_add_inquilino = tk.Button(win_inquilinos, text="Agregar Inquilino", command=add_inquilino)
        btn_add_inquilino.pack(fill=tk.X, padx=10, pady=5)

        btn_del_inquilino = tk.Button(win_inquilinos, text="Eliminar Inquilino", command=del_inquilino)
        btn_del_inquilino.pack(fill=tk.X, padx=10, pady=5)

        load_inquilinos()

    def show_pagos_mantenimiento(self):
        # Ventana para mostrar y gestionar pagos de mantenimiento
        def load_pagos_mantenimiento():
            for row in self.pagos_list.get_children():
                self.pagos_list.delete(row)
            pagos = obtener_pagos_mantenimiento()
            for pago in pagos:
                self.pagos_list.insert('', 'end', values=(pago['id'], pago['nombre_completo'], pago['mes'], pago['monto']))

        def add_pago():
            # Ventana para agregar un nuevo pago de mantenimiento
            def save_pago():
                inquilino_id = inquilinos_combobox.get().split()[0]
                mes = entry_mes.get()
                monto = entry_monto.get()
                if inquilino_id and mes and monto:
                    registrar_pago_mantenimiento(inquilino_id, mes, float(monto))
                    messagebox.showinfo("Éxito", "Pago registrado correctamente")
                    win_add_pago.destroy()
                    load_pagos_mantenimiento()
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

        win_pagos_mantenimiento = tk.Toplevel(self.root)
        win_pagos_mantenimiento.title("Pagos de Mantenimiento")

        self.pagos_list = ttk.Treeview(win_pagos_mantenimiento, columns=('ID', 'Inquilino', 'Mes', 'Monto'), show='headings')
        self.pagos_list.heading('ID', text='ID')
        self.pagos_list.heading('Inquilino', text='Inquilino')
        self.pagos_list.heading('Mes', text='Mes')
        self.pagos_list.heading('Monto', text='Monto')
        self.pagos_list.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        btn_add_pago = tk.Button(win_pagos_mantenimiento, text="Registro de Pagos", command=add_pago)
        btn_add_pago.pack(fill=tk.X, padx=10, pady=5)

        load_pagos_mantenimiento()

    def show_pagos_proveedores(self):
        # Ventana para mostrar y gestionar pagos a proveedores
        def load_pagos_proveedores():
            for row in self.proveedores_list.get_children():
                self.proveedores_list.delete(row)
            pagos = obtener_pagos_proveedores()
            for pago in pagos:
                self.proveedores_list.insert('', 'end', values=(pago['id'], pago['proveedor'], pago['fecha'], pago['monto']))

        def add_proveedor():
            # Ventana para agregar un nuevo pago a proveedor
            def save_proveedor():
                proveedor = entry_proveedor.get()
                fecha = entry_fecha.get()
                monto = entry_monto.get()
                if proveedor and fecha and monto:
                    registrar_pago_proveedor(proveedor, fecha, float(monto))
                    messagebox.showinfo("Éxito", "Pago a proveedor registrado correctamente")
                    win_add_proveedor.destroy()
                    load_pagos_proveedores()
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

        win_pagos_proveedores = tk.Toplevel(self.root)
        win_pagos_proveedores.title("Pagos a Proveedores")

        self.proveedores_list = ttk.Treeview(win_pagos_proveedores, columns=('ID', 'Proveedor', 'Fecha', 'Monto'), show='headings')
        self.proveedores_list.heading('ID', text='ID')
        self.proveedores_list.heading('Proveedor', text='Proveedor')
        self.proveedores_list.heading('Fecha', text='Fecha')
        self.proveedores_list.heading('Monto', text='Monto')
        self.proveedores_list.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        btn_add_proveedor = tk.Button(win_pagos_proveedores, text="Registro de Pagos a Proveedores", command=add_proveedor)
        btn_add_proveedor.pack(fill=tk.X, padx=10, pady=5)

        load_pagos_proveedores()

    def gen_cupon(self):
        # Ventana para generar cupón de pago
        def generate_cupon():
            inquilino_seleccionado = inquilinos_combobox.get()
            mes = entry_mes.get()
            if not inquilino_seleccionado or not mes:
                messagebox.showwarning("Error", "Debe seleccionar un inquilino y especificar el mes")
                return

            inquilino_id = inquilino_seleccionado.split()[0]
            inquilino_nombre = inquilino_seleccionado.split(' - ')[1]

            monto = obtener_monto_pago_actual(inquilino_id, mes)
            if monto is None:
                messagebox.showwarning("Error", f"No se encontró un pago para el inquilino {inquilino_nombre} en el mes de {mes}")
                return

            ruta_archivo = f"cupon_{inquilino_nombre}_{mes}.pdf"
            inquilino = {'id': inquilino_id, 'nombre_completo': inquilino_nombre}
            generar_cupon_pago(inquilino, mes, monto, ruta_archivo)

            messagebox.showinfo("Éxito", f"Cupon de pago generado: {ruta_archivo}")

        win_gen_cupon = tk.Toplevel(self.root)
        win_gen_cupon.title("Generar Cupon de Pago")

        inquilinos = obtener_inquilinos()

        label_inquilino = tk.Label(win_gen_cupon, text="Inquilino")
        label_inquilino.pack(pady=10)
        inquilinos_combobox = ttk.Combobox(win_gen_cupon, values=[f"{i['id']} - {i['nombre_completo']}" for i in inquilinos])
        inquilinos_combobox.pack(pady=10)

        label_mes = tk.Label(win_gen_cupon, text="Mes")
        label_mes.pack(pady=10)
        entry_mes = tk.Entry(win_gen_cupon)
        entry_mes.pack(pady=10)

        btn_generate = tk.Button(win_gen_cupon, text="Generar", command=generate_cupon)
        btn_generate.pack(pady=10)

    def gen_certificado(self):
        # Ventana para generar certificado de estado
        def generate_certificado():
            inquilino_seleccionado = inquilinos_combobox.get()
            if not inquilino_seleccionado:
                messagebox.showwarning("Error", "Debe seleccionar un inquilino")
                return

            inquilino_id = inquilino_seleccionado.split()[0]
            inquilino_nombre = inquilino_seleccionado.split(' - ')[1]

            ruta_archivo = f"certificado_estado_{inquilino_nombre}.pdf"

            inquilino = {'id': inquilino_id, 'nombre_completo': inquilino_nombre}
            pagos = obtener_pagos_por_inquilino(inquilino_id)
            generar_certificado_estado(inquilino, pagos, ruta_archivo)

            messagebox.showinfo("Éxito", f"Certificado de estado generado: {ruta_archivo}")

        win_gen_certificado = tk.Toplevel(self.root)
        win_gen_certificado.title("Generar Certificado de Estado")

        inquilinos = obtener_inquilinos()

        label_inquilino = tk.Label(win_gen_certificado, text="Inquilino")
        label_inquilino.pack(pady=10)
        inquilinos_combobox = ttk.Combobox(win_gen_certificado, values=[f"{i['id']} - {i['nombre_completo']}" for i in inquilinos])
        inquilinos_combobox.pack(pady=10)

        btn_generate = tk.Button(win_gen_certificado, text="Generar", command=generate_certificado)
        btn_generate.pack(pady=10)

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
                signed_doc_path = self.save_signed_document(document_path, document_data, signature)
                self.guardar_documento_firmado(document_path, signed_doc_path, signature)

                messagebox.showinfo("Éxito", "Documento firmado y guardado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al firmar el documento: {str(e)}")

    def save_signed_document(self, document_path, document_data, signature):
        signed_doc_path = f"{document_path}.signed.pdf"
        with open(signed_doc_path, "wb") as signed_doc:
            signed_doc.write(document_data)  # Escribir el documento original
            signed_doc.write(signature)  # Adjuntar la firma al final
        return signed_doc_path

    def guardar_documento_firmado(self, original_path, signed_path, signature):
        nombre = os.path.basename(original_path)
        url = os.path.abspath(signed_path)
        guardar_documento_firmado(nombre, url, signature)

    def load_proveedores(self):
        # Cargar la lista de pagos a proveedores desde la base de datos
        for row in self.proveedores_list.get_children():
            self.proveedores_list.delete(row)
        proveedores = obtener_pagos_proveedores()
        for proveedor in proveedores:
            self.proveedores_list.insert('', 'end', values=(proveedor['id'], proveedor['proveedor'], proveedor['fecha'], proveedor['monto']))
