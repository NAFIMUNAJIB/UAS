import customtkinter as ctk
from tkinter import ttk, messagebox
from barang import ambil_semua_barang, tambah_barang_gui, ambil_stok_menipis
from transaksi import catat_transaksi_gui, ambil_riwayat_transaksi

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, user_data: dict, on_logout):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.user_data = user_data
        self.on_logout = on_logout

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.buat_sidebar()

        self.main_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.tampilkan_dashboard()
        self.after(400, self.cek_alert_awal)

    def buat_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)

        ctk.CTkLabel(
            self.sidebar, text="📦 INVENTARIS\nPRO SYSTEM",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(25, 15))

        # Info Profil Petugas yang Sedang Login
        user_box = ctk.CTkFrame(self.sidebar, corner_radius=10, fg_color=("gray85", "gray20"))
        user_box.grid(row=1, column=0, padx=15, pady=(0, 20), sticky="ew")
        ctk.CTkLabel(
            user_box, text=f"👤 {self.user_data['nama_lengkap']}",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=12, pady=(8, 0))
        ctk.CTkLabel(
            user_box, text=f"Role: {self.user_data['peran'].upper()}",
            font=ctk.CTkFont(size=11), text_color="gray"
        ).pack(anchor="w", padx=12, pady=(0, 8))

        btn_style = {"height": 42, "corner_radius": 8, "anchor": "w", "font": ctk.CTkFont(size=14)}

        ctk.CTkButton(self.sidebar, text="  📊  Dashboard & Stok", command=self.tampilkan_dashboard, **btn_style).grid(row=2, column=0, padx=15, pady=5, sticky="ew")
        ctk.CTkButton(self.sidebar, text="  ➕  Tambah Barang Baru", command=self.tampilkan_tambah_barang, **btn_style).grid(row=3, column=0, padx=15, pady=5, sticky="ew")
        ctk.CTkButton(self.sidebar, text="  🔄  Transaksi Masuk/Keluar", command=self.tampilkan_transaksi, **btn_style).grid(row=4, column=0, padx=15, pady=5, sticky="ew")
        ctk.CTkButton(self.sidebar, text="  📜  Riwayat Transaksi", command=self.tampilkan_riwayat, **btn_style).grid(row=5, column=0, padx=15, pady=5, sticky="ew")

        # Switch Tema Dark/Light
        self.theme_switch = ctk.CTkSwitch(self.sidebar, text="Mode Gelap", command=self.ganti_tema)
        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()
        else:
            self.theme_switch.configure(text="Mode Terang")
        self.theme_switch.grid(row=8, column=0, padx=20, pady=(10, 10), sticky="w")

        # Tombol Logout
        ctk.CTkButton(
            self.sidebar, text="🚪  Keluar (Logout)", height=40, corner_radius=8,
            fg_color="#d9534f", hover_color="#c9302c", font=ctk.CTkFont(size=13, weight="bold"),
            command=self.konfirmasi_logout
        ).grid(row=9, column=0, padx=15, pady=(5, 20), sticky="ew")

    def konfirmasi_logout(self):
        if messagebox.askyesno("Konfirmasi Logout", "Apakah Anda yakin ingin keluar dari sesi ini?"):
            self.on_logout()

    def ganti_tema(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
            self.theme_switch.configure(text="Mode Gelap")
        else:
            ctk.set_appearance_mode("Light")
            self.theme_switch.configure(text="Mode Terang")

    def bersihkan_halaman(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def cek_alert_awal(self):
        menipis = ambil_stok_menipis()
        if menipis:
            daftar = "\n".join([f"- {b['nama_barang']} (Sisa: {b['stok']}, Min: {b['stok_minimum']})" for b in menipis])
            messagebox.showwarning("Peringatan Stok Menipis!", f"Beberapa barang mencapai batas stok minimum:\n\n{daftar}")

    def tampilkan_dashboard(self):
        self.bersihkan_halaman()

        data_barang = ambil_semua_barang()
        data_menipis = ambil_stok_menipis()
        total_item = len(data_barang)
        total_stok = sum(b['stok'] for b in data_barang)

        top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        top_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.buat_kartu_stat(top_frame, 0, "Total Jenis Barang", f"{total_item} Item", "#1f6aa5")
        self.buat_kartu_stat(top_frame, 1, "Total Unit di Gudang", f"{total_stok} Unit", "#2fa572")
        self.buat_kartu_stat(top_frame, 2, "Peringatan Stok Menipis", f"{len(data_menipis)} Item", "#d9534f" if data_menipis else "#2fa572")

        table_container = ctk.CTkFrame(self.main_frame, corner_radius=10)
        table_container.grid(row=1, column=0, sticky="nsew")
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(table_container, text="Daftar Inventaris & Stok Barang Terkini", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=20, pady=15)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=32, fieldbackground="#2b2b2b", borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#1f6aa5", foreground="white", relief="flat", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#144870")])

        kolom = ("id", "kode", "nama", "kategori", "supplier", "stok", "min", "harga")
        tree = ttk.Treeview(table_container, columns=kolom, show="headings")

        headings = [
            ("id", "ID", 45), ("kode", "Kode", 90), ("nama", "Nama Barang", 200),
            ("kategori", "Kategori", 140), ("supplier", "Supplier", 140),
            ("stok", "Stok", 70), ("min", "Batas Min", 80), ("harga", "Harga Jual", 120)
        ]
        for col, text, width in headings:
            tree.heading(col, text=text)
            tree.column(col, width=width, anchor="center" if col in ["id", "kode", "stok", "min"] else "w")

        for b in data_barang:
            status_tag = "menipis" if b['stok'] <= b['stok_minimum'] else "aman"
            tree.insert("", "end", values=(
                b['id_barang'], b['kode_barang'], b['nama_barang'],
                b['kategori'], b['supplier'], b['stok'], b['stok_minimum'],
                f"Rp {b['harga_jual']:,.0f}"
            ), tags=(status_tag,))

        tree.tag_configure("menipis", background="#5c2323")
        tree.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

    def buat_kartu_stat(self, parent, col, judul, nilai, warna):
        card = ctk.CTkFrame(parent, corner_radius=10, fg_color=warna)
        card.grid(row=0, column=col, sticky="ew", padx=6)
        ctk.CTkLabel(card, text=judul, font=ctk.CTkFont(size=13), text_color="white").pack(anchor="w", padx=18, pady=(14, 2))
        ctk.CTkLabel(card, text=nilai, font=ctk.CTkFont(size=24, weight="bold"), text_color="white").pack(anchor="w", padx=18, pady=(0, 14))

    def tampilkan_tambah_barang(self):
        self.bersihkan_halaman()

        form_card = ctk.CTkFrame(self.main_frame, corner_radius=12)
        form_card.grid(row=0, column=0, sticky="nsew", padx=40, pady=10)
        form_card.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(form_card, text="Pendaftaran Master Barang Baru", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, pady=(20, 20))

        fields = {}
        input_list = [
            ("Kode Barang (Contoh: BRG002)", "kode", 1, 0),
            ("Nama Barang", "nama", 1, 1),
            ("ID Kategori (Contoh: 1)", "kategori", 2, 0),
            ("ID Supplier (Isi 0 jika tidak ada)", "supplier", 2, 1),
            ("Jumlah Stok Awal", "stok", 3, 0),
            ("Batas Stok Minimum (Alert)", "min", 3, 1),
            ("Harga Beli (Rp)", "h_beli", 4, 0),
            ("Harga Jual (Rp)", "h_jual", 4, 1),
        ]

        for label_text, key, r, c in input_list:
            frame_in = ctk.CTkFrame(form_card, fg_color="transparent")
            frame_in.grid(row=r, column=c, sticky="ew", padx=20, pady=8)
            ctk.CTkLabel(frame_in, text=label_text, font=ctk.CTkFont(size=13)).pack(anchor="w")
            entry = ctk.CTkEntry(frame_in, height=38, placeholder_text=label_text)
            entry.pack(fill="x", pady=(4, 0))
            fields[key] = entry

        def simpan():
            try:
                sukses, pesan = tambah_barang_gui(
                    fields["kode"].get().strip(),
                    fields["nama"].get().strip(),
                    int(fields["kategori"].get()),
                    int(fields["supplier"].get()),
                    int(fields["stok"].get()),
                    int(fields["min"].get()),
                    float(fields["h_beli"].get()),
                    float(fields["h_jual"].get())
                )
                if sukses:
                    messagebox.showinfo("Berhasil", pesan)
                    self.tampilkan_dashboard()
                else:
                    messagebox.showerror("Gagal", pesan)
            except ValueError:
                messagebox.showerror("Input Error", "Pastikan kolom angka (ID, Stok, Harga) diisi dengan angka yang valid!")

        ctk.CTkButton(form_card, text="💾 Simpan Data Barang", height=44, font=ctk.CTkFont(size=14, weight="bold"), command=simpan).grid(row=5, column=0, columnspan=2, padx=20, pady=25, sticky="ew")

    def tampilkan_transaksi(self):
        self.bersihkan_halaman()

        trans_card = ctk.CTkFrame(self.main_frame, corner_radius=12)
        trans_card.grid(row=0, column=0, sticky="nsew", padx=80, pady=10)
        trans_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(trans_card, text="Pencatatan Transaksi Stok (Masuk / Keluar)", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(25, 10))

        # Menampilkan Petugas yang Otomatis Terdeteksi dari Sesi Login
        ctk.CTkLabel(
            trans_card,
            text=f"Petugas Aktif: {self.user_data['nama_lengkap']} (ID: {self.user_data['id_pengguna']})",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2fa572"
        ).pack(pady=(0, 15))

        ctk.CTkLabel(trans_card, text="Jenis Transaksi:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=40)
        jenis_var = ctk.StringVar(value="masuk")
        ctk.CTkSegmentedButton(trans_card, values=["masuk", "keluar"], variable=jenis_var, height=38).pack(fill="x", padx=40, pady=(4, 15))

        ctk.CTkLabel(trans_card, text="ID Barang:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=40)
        entry_id_barang = ctk.CTkEntry(trans_card, height=38, placeholder_text="Masukkan ID Barang (Contoh: 1)")
        entry_id_barang.pack(fill="x", padx=40, pady=(4, 15))

        ctk.CTkLabel(trans_card, text="Jumlah Unit:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=40)
        entry_jumlah = ctk.CTkEntry(trans_card, height=38, placeholder_text="Masukkan jumlah unit barang")
        entry_jumlah.pack(fill="x", padx=40, pady=(4, 15))

        ctk.CTkLabel(trans_card, text="Keterangan / Catatan:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=40)
        entry_ket = ctk.CTkEntry(trans_card, height=38, placeholder_text="Contoh: Restok supplier / Penjualan toko")
        entry_ket.pack(fill="x", padx=40, pady=(4, 20))

        def proses():
            try:
                sukses, pesan = catat_transaksi_gui(
                    int(entry_id_barang.get()),
                    self.user_data['id_pengguna'],  # Otomatis mengambil ID dari user yang login
                    jenis_var.get(),
                    int(entry_jumlah.get()),
                    entry_ket.get().strip()
                )
                if sukses:
                    messagebox.showinfo("Transaksi Sukses", pesan)
                    self.tampilkan_dashboard()
                else:
                    messagebox.showerror("Transaksi Gagal", pesan)
            except ValueError:
                messagebox.showerror("Error", "ID Barang dan Jumlah Unit harus berupa angka!")

        ctk.CTkButton(trans_card, text="✅ Proses Transaksi Stok", height=44, font=ctk.CTkFont(size=14, weight="bold"), command=proses).pack(fill="x", padx=40, pady=(5, 25))

    def tampilkan_riwayat(self):
        self.bersihkan_halaman()

        history_container = ctk.CTkFrame(self.main_frame, corner_radius=10)
        history_container.grid(row=0, column=0, rowspan=2, sticky="nsew")
        history_container.grid_columnconfigure(0, weight=1)
        history_container.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(history_container, text="Riwayat Log Transaksi Barang Masuk & Keluar", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=20, pady=15)

        kolom = ("id", "tanggal", "kode", "nama", "jenis", "jumlah", "petugas", "ket")
        tree = ttk.Treeview(history_container, columns=kolom, show="headings")

        headings = [
            ("id", "ID", 45), ("tanggal", "Waktu Transaksi", 150), ("kode", "Kode", 80),
            ("nama", "Nama Barang", 170), ("jenis", "Jenis", 80), ("jumlah", "Jumlah", 70),
            ("petugas", "Petugas", 120), ("ket", "Keterangan", 180)
        ]
        for col, text, width in headings:
            tree.heading(col, text=text)
            tree.column(col, width=width, anchor="center" if col in ["id", "kode", "jenis", "jumlah"] else "w")

        for t in ambil_riwayat_transaksi():
            tree.insert("", "end", values=(
                t['id_transaksi'], str(t['tanggal_transaksi']), t['kode_barang'],
                t['nama_barang'], t['jenis_transaksi'].upper(), t['jumlah'],
                t['petugas'], t['keterangan']
            ))

        tree.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))