from db_config import get_connection

def catat_transaksi_gui(id_barang, id_pengguna, jenis, jumlah, keterangan=""):
    conn = get_connection()
    if not conn:
        return False, "Koneksi database terputus!"
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT stok, nama_barang FROM barang WHERE id_barang = %s", (id_barang,))
        barang = cursor.fetchone()
        
        if not barang:
            return False, "ID Barang tidak ditemukan di database!"

        stok_sekarang = barang['stok']

        if jenis == 'keluar' and jumlah > stok_sekarang:
            return False, f"Stok tidak cukup! Sisa stok '{barang['nama_barang']}' hanya {stok_sekarang}."

        query_trans = """
            INSERT INTO transaksi_stok (id_barang, id_pengguna, jenis_transaksi, jumlah, keterangan)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_trans, (id_barang, id_pengguna, jenis, jumlah, keterangan))

        stok_baru = stok_sekarang + jumlah if jenis == 'masuk' else stok_sekarang - jumlah
        cursor.execute("UPDATE barang SET stok = %s WHERE id_barang = %s", (stok_baru, id_barang))

        conn.commit()
        return True, f"Transaksi {jenis.upper()} berhasil!\nStok '{barang['nama_barang']}' sekarang: {stok_baru}"

    except Exception as e:
        conn.rollback()
        return False, f"Terjadi kesalahan: {e}"
    finally:
        cursor.close()
        conn.close()

def ambil_riwayat_transaksi():
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT t.id_transaksi, b.kode_barang, b.nama_barang, t.jenis_transaksi, 
                   t.jumlah, t.tanggal_transaksi, p.nama_lengkap AS petugas, t.keterangan
            FROM transaksi_stok t
            JOIN barang b ON t.id_barang = b.id_barang
            JOIN pengguna p ON t.id_pengguna = p.id_pengguna
            ORDER BY t.tanggal_transaksi DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception:
        return []
    finally:
        cursor.close()
        conn.close()