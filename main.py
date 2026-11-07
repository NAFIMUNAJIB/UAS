import sys
from barang import tambah_barang, lihat_semua_barang, cek_stok_menipis
from transaksi import catat_transaksi_stok, lihat_riwayat_transaksi

def menu_utama():
    while True:
        print("\n" + "=" * 50)
        print("  SISTEM INVENTARIS & MANAJEMEN STOK BARANG")
        print("=" * 50)
        print(" 1. Lihat Daftar Stok Barang")
        print(" 2. Tambah Barang Baru")
        print(" 3. Transaksi Barang Masuk (Restok)")
        print(" 4. Transaksi Barang Keluar")
        print(" 5. Riwayat Transaksi Masuk")
        print(" 6. Riwayat Transaksi Keluar")
        print(" 7. Cek Peringatan Stok Menipis")
        print(" 8. Keluar Program")
        print("=" * 50)

        pilihan = input("Pilih menu (1-8): ").strip()

        if pilihan == '1':
            lihat_semua_barang()
        elif pilihan == '2':
            print("\n--- Tambah Barang Baru ---")
            kode = input("Masukkan Kode Barang  : ").strip()
            nama = input("Masukkan Nama Barang  : ").strip()
            id_kategori = int(input("Masukkan ID Kategori : "))
            id_supplier = int(input("Masukkan ID Supplier (Isi 0 jika tidak ada) : "))
            stok = int(input("Jumlah Stok Awal     : "))
            stok_min = int(input("Batas Stok Minimum   : "))
            h_beli = float(input("Harga Beli (Rp)      : "))
            h_jual = float(input("Harga Jual (Rp)      : "))
            tambah_barang(kode, nama, id_kategori, id_supplier, stok, stok_min, h_beli, h_jual)
        elif pilihan == '3':
            print("\n--- Transaksi Barang Masuk ---")
            id_b = int(input("Masukkan ID Barang : "))
            id_p = int(input("Masukkan ID Petugas: "))
            jml = int(input("Jumlah Masuk       : "))
            ket = input("Keterangan         : ")
            catat_transaksi_stok(id_b, id_p, 'masuk', jml, ket)
        elif pilihan == '4':
            print("\n--- Transaksi Barang Keluar ---")
            id_b = int(input("Masukkan ID Barang : "))
            id_p = int(input("Masukkan ID Petugas: "))
            jml = int(input("Jumlah Keluar      : "))
            ket = input("Keterangan         : ")
            catat_transaksi_stok(id_b, id_p, 'keluar', jml, ket)
        elif pilihan == '5':
            lihat_riwayat_transaksi('masuk')
        elif pilihan == '6':
            lihat_riwayat_transaksi('keluar')
        elif pilihan == '7':
            cek_stok_menipis()
        elif pilihan == '8':
            print("\n[✓] Terima kasih, program selesai!")
            sys.exit()
        else:
            print("[!] Pilihan menu tidak valid!")

if __name__ == "__main__":
    menu_utama()