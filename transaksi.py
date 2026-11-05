from db_config import get_connection

def catat_transaksi_stok(id_barang, id_pengguna, jenis, jumlah, keterangan=""):
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor(dictionary=True)

        # 1. Cek stok awal
        cursor.execute("SELECT stok, nama_barang FROM barang WHERE id_barang = %s", (id_barang,))
        barang = cursor.fetchone()
        
        if not barang:
            print("[!] ID Barang tidak ditemukan!")
            return

        stok_sekarang = barang['stok']

        # Validasi jika barang keluar tapi stok kurang
        if jenis == 'keluar' and jumlah > stok_sekarang:
            print(f"[!] Transaksi Gagal! Stok '{barang['nama_barang']}' hanya tersisa {stok_sekarang}.")
            return

        # 2. Catat riwayat di tabel transaksi_stok
        query_trans = """
            INSERT INTO transaksi_stok (id_barang, id_pengguna, jenis_transaksi, jumlah, keterangan)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_trans, (id_barang, id_pengguna, jenis, jumlah, keterangan))

        # 3. Update jumlah stok fisik di tabel barang
        if jenis == 'masuk':
            stok_baru = stok_sekarang + jumlah
        else:
            stok_baru = stok_sekarang - jumlah

        cursor.execute("UPDATE barang SET stok = %s WHERE id_barang = %s", (stok_baru, id_barang))

        conn.commit()
        print(f"[✓] Transaksi {jenis.upper()} berhasil! Stok '{barang['nama_barang']}' sekarang: {stok_baru}")

    except Exception as e:
        conn.rollback()
        print(f"[!] Gagal memproses transaksi: {e}")
    finally:
        cursor.close()
        conn.close()