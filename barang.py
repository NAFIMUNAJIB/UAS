from db_config import get_connection

def ambil_semua_barang():
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT b.id_barang, b.kode_barang, b.nama_barang, 
                   COALESCE(k.nama_kategori, '-') AS kategori, 
                   COALESCE(s.nama_supplier, '-') AS supplier, 
                   b.stok, b.stok_minimum, b.harga_beli, b.harga_jual
            FROM barang b
            LEFT JOIN kategori k ON b.id_kategori = k.id_kategori
            LEFT JOIN supplier s ON b.id_supplier = s.id_supplier
            ORDER BY b.id_barang ASC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error ambil data: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def tambah_barang_gui(kode, nama, id_kategori, id_supplier, stok, stok_minimum, harga_beli, harga_jual):
    conn = get_connection()
    if not conn:
        return False, "Gagal terhubung ke database!"
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO barang (kode_barang, nama_barang, id_kategori, id_supplier, stok, stok_minimum, harga_beli, harga_jual)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (kode, nama, id_kategori, id_supplier if id_supplier != 0 else None, stok, stok_minimum, harga_beli, harga_jual)
        cursor.execute(query, values)
        conn.commit()
        return True, f"Barang '{nama}' berhasil ditambahkan!"
    except Exception as e:
        return False, f"Gagal menambah barang: {e}"
    finally:
        cursor.close()
        conn.close()

def ambil_stok_menipis():
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id_barang, kode_barang, nama_barang, stok, stok_minimum FROM barang WHERE stok <= stok_minimum"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception:
        return []
    finally:
        cursor.close()
        conn.close()