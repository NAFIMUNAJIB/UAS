import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Sesuaikan jika password MySQL XAMPP kamu diisi
            database='db_inventaris_stok'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"[!] Gagal terhubung ke basis data MySQL: {e}")
        return None