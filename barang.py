from db_config import get_connection

def tambah_barang(kode, nama, id_kategori, id_supplier, stok, stok_minimum, harga_beli, harga_jual):
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO barang (kode_barang, nama_barang, id_kategori, id_supplier, stok, stok_minimum, harga_beli, harga_jual)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (kode, nama, id_kategori, id_supplier if id_supplier != 0 else None, stok, stok_minimum, harga_beli, harga_jual)
        cursor.execute(query, values)
        conn.commit()
        print(f"[✓] Barang '{nama}' berhasil ditambahkan!")
    except Exception as e:
        print(f"[!] Gagal menambah barang: {e}")
    finally:
        cursor.close()
        conn.close()

def lihat_semua_barang():
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT b.id_barang, b.kode_barang, b.nama_barang, 
                   COALESCE(k.nama_kategori, '-') AS kategori, 
                   COALESCE(s.nama_supplier, '-') AS supplier, 
                   b.stok, b.stok_minimum, b.harga_jual
            FROM barang b
            LEFT JOIN kategori k ON b.id_kategori = k.id_kategori
            LEFT JOIN supplier s ON b.id_supplier = s.id_supplier
            ORDER BY b.id_barang ASC
        """
        cursor.execute(query)
        results = cursor.fetchall()

        print("\n" + "=" * 90)
        print("                                DAFTAR STOK BARANG")
        print("=" * 90)
        print(f"{'ID':<4} | {'Kode':<10} | {'Nama Barang':<20} | {'Kategori':<15} | {'Stok':<6} | {'Min':<5} | {'Harga Jual':<12}")
        print("-" * 90)
        for r in results:
            print(f"{r['id_barang']:<4} | {r['kode_barang']:<10} | {r['nama_barang']:<20} | {r['kategori']:<15} | {r['stok']:<6} | {r['stok_minimum']:<5} | Rp {r['harga_jual']:>9,}")
        print("=" * 90)
    except Exception as e:
        print(f"[!] Gagal mengambil data barang: {e}")
    finally:
        cursor.close()
        conn.close()

def cek_stok_menipis():
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT kode_barang, nama_barang, stok, stok_minimum FROM barang WHERE stok <= stok_minimum"
        cursor.execute(query)
        results = cursor.fetchall()

        print("\n" + "!" * 65)
        print("            PERINGATAN STOK MENIPIS / HABIS")
        print("!" * 65)
        if not results:
            print(" [✓] Semua stok barang dalam kondisi aman.")
        else:
            for r in results:
                print(f" [!] {r['nama_barang']} ({r['kode_barang']}) -> Sisa Stok: {r['stok']} (Batas Min: {r['stok_minimum']})")
        print("!" * 65)
    except Exception as e:
        print(f"[!] Error cek stok: {e}")
    finally:
        cursor.close()
        conn.close()