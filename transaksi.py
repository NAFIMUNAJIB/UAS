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


def lihat_riwayat_transaksi(jenis):
    if jenis not in ('masuk', 'keluar'):
        print("[!] Jenis transaksi tidak valid.")
        return

    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT t.*, b.nama_barang
            FROM transaksi_stok t
            LEFT JOIN barang b ON t.id_barang = b.id_barang
            WHERE t.jenis_transaksi = %s
            ORDER BY t.id_transaksi DESC
        """
        cursor.execute(query, (jenis,))
        results = cursor.fetchall()

        print("\n" + "=" * 70)
        print(f"RIWAYAT TRANSAKSI BARANG {jenis.upper()}")
        print("=" * 70)
        if not results:
            print("Belum ada riwayat transaksi.")
        else:
            for transaksi in results:
                print("-" * 70)
                for kolom, nilai in transaksi.items():
                    label = kolom.replace("_", " ").title()
                    print(f"{label:<22}: {nilai}")
        print("=" * 70)
    except Exception as e:
        print(f"[!] Gagal mengambil riwayat transaksi: {e}")
    finally:
        cursor.close()
        conn.close()