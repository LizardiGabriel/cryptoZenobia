import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Obtener conexión a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect('condominio.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear las tablas necesarias en la base de datos
def create_database():
    conn = get_db_connection()
    c = conn.cursor()


    c.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS inquilinos (
            id INTEGER PRIMARY KEY,
            nombre_completo TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS pagos_mantenimiento (
            id INTEGER PRIMARY KEY,
            inquilino_id INTEGER NOT NULL,
            mes TEXT NOT NULL,
            monto REAL NOT NULL,
            FOREIGN KEY (inquilino_id) REFERENCES inquilinos (id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS pagos_proveedores (
            id INTEGER PRIMARY KEY,
            proveedor TEXT NOT NULL,
            fecha TEXT NOT NULL,
            monto REAL NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS documentos_firmados (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            url TEXT NOT NULL,
            firma BLOB NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def registrar_admin(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    password_hash = generate_password_hash(password)
    try:
        c.execute('INSERT INTO admin (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def verificar_admin(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT password_hash FROM admin WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    if user and check_password_hash(user['password_hash'], password):
        return True
    return False

# Agregar un inquilino a la base de datos
def agregar_inquilino(nombre_completo: str):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO inquilinos (nombre_completo) VALUES (?)', (nombre_completo,))
    conn.commit()
    conn.close()

# Eliminar un inquilino y sus pagos asociados de la base de datos
def eliminar_inquilino(inquilino_id: int):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM inquilinos WHERE id = ?', (inquilino_id,))
    c.execute('DELETE FROM pagos_mantenimiento WHERE inquilino_id = ?', (inquilino_id,))
    conn.commit()
    conn.close()

# Registrar un pago de mantenimiento para un inquilino
def registrar_pago_mantenimiento(inquilino_id: int, mes: str, monto: float):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO pagos_mantenimiento (inquilino_id, mes, monto) 
        VALUES (?, ?, ?)
    ''', (inquilino_id, mes, monto))
    conn.commit()
    conn.close()

# Registrar un pago a un proveedor
def registrar_pago_proveedor(proveedor: str, fecha: str, monto: float):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO pagos_proveedores (proveedor, fecha, monto) 
        VALUES (?, ?, ?)
    ''', (proveedor, fecha, monto))
    conn.commit()
    conn.close()

# Obtener la lista de inquilinos
def obtener_inquilinos():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM inquilinos')
    inquilinos = c.fetchall()
    conn.close()
    return inquilinos

# Obtener la lista de pagos de mantenimiento
def obtener_pagos_mantenimiento():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT pm.id, i.nombre_completo, pm.mes, pm.monto FROM pagos_mantenimiento pm JOIN inquilinos i ON pm.inquilino_id = i.id')
    pagos = c.fetchall()
    conn.close()
    return pagos

# Obtener la lista de pagos a proveedores
def obtener_pagos_proveedores():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM pagos_proveedores')
    proveedores = c.fetchall()
    conn.close()
    return proveedores

# Obtener los pagos de un inquilino específico
def obtener_pagos_por_inquilino(inquilino_id: int):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM pagos_mantenimiento WHERE inquilino_id = ?', (inquilino_id,))
    pagos = c.fetchall()
    conn.close()
    return pagos

# Obtener el monto de pago del mes actual para un inquilino
def obtener_monto_pago_actual(inquilino_id: int, mes: str):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT monto FROM pagos_mantenimiento WHERE inquilino_id = ? AND mes = ?', (inquilino_id, mes))
    pago = c.fetchone()
    conn.close()
    return pago['monto'] if pago else None

# Guardar la URL del documento firmado en la base de datos
def guardar_documento_firmado(nombre, url, firma):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO documentos_firmados (nombre, url, firma) 
        VALUES (?, ?, ?)
    ''', (nombre, url, firma))
    conn.commit()
    conn.close()
