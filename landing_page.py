import webbrowser
import customtkinter as ctk

class LandingPageFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_click, on_register_click):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.on_login_click = on_login_click
        self.on_register_click = on_register_click

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.buat_navbar()
        self.buat_konten_utama()
        self.buat_footer()

    def buat_navbar(self):
        navbar = ctk.CTkFrame(self, height=70, corner_radius=0)
        navbar.grid(row=0, column=0, sticky="ew")
        navbar.grid_columnconfigure(1, weight=1)

        # Brand Logo / Judul
        brand = ctk.CTkLabel(
            navbar,
            text="📦  INVENTARIS PRO SYSTEM",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        brand.grid(row=0, column=0, padx=30, pady=18, sticky="w")

        # Tombol Navigasi Kanan (Login & Register)
        nav_buttons = ctk.CTkFrame(navbar, fg_color="transparent")
        nav_buttons.grid(row=0, column=2, padx=30, pady=15, sticky="e")

        btn_login = ctk.CTkButton(
            nav_buttons,
            text="Masuk (Login)",
            width=130,
            height=38,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90"),
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_login_click
        )
        btn_login.pack(side="left", padx=(0, 10))

        btn_register = ctk.CTkButton(
            nav_buttons,
            text="Daftar (Register)",
            width=140,
            height=38,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_register_click
        )
        btn_register.pack(side="left")

    def buat_konten_utama(self):
        scroll_area = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_area.grid(row=1, column=0, sticky="nsew", padx=40, pady=15)
        scroll_area.grid_columnconfigure(0, weight=1)

        #Banner
        hero_card = ctk.CTkFrame(scroll_area, corner_radius=16, fg_color=("#1f6aa5", "#144870"))
        hero_card.grid(row=0, column=0, sticky="ew", pady=(10, 20))
        hero_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            hero_card,
            text="Sistem Inventaris & Manajemen Stok Barang Terpadu",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).pack(pady=(35, 10), padx=30)

        ctk.CTkLabel(
            hero_card,
            text="Solusi digital modern untuk memantau ketersediaan stok gudang, mencatat arus barang masuk & keluar,\nserta mencegah kekosongan stok secara real-time.",
            font=ctk.CTkFont(size=15),
            text_color="#e0e0e0",
            justify="center"
        ).pack(pady=(0, 25), padx=30)

        cta_frame = ctk.CTkFrame(hero_card, fg_color="transparent")
        cta_frame.pack(pady=(0, 35))

        ctk.CTkButton(
            cta_frame,
            text="Mulai Kelola Stok Sekarang  →",
            height=44,
            width=230,
            fg_color="#2fa572",
            hover_color="#248259",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.on_login_click
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            cta_frame,
            text="Buat Akun Petugas",
            height=44,
            width=180,
            fg_color="white",
            text_color="#144870",
            hover_color="#e6e6e6",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.on_register_click
        ).pack(side="left", padx=8)

        # 2. Bagian About Me / Tentang Sistem
        about_card = ctk.CTkFrame(scroll_area, corner_radius=14)
        about_card.grid(row=1, column=0, sticky="ew", pady=(0, 20))

        ctk.CTkLabel(
            about_card,
            text="Tentang Sistem (About Us)",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w", padx=30, pady=(25, 10))

        deskripsi_about = (
            "Inventaris Pro System adalah aplikasi manajemen inventaris berbasis desktop yang terintegrasi langsung "
            "dengan basis data relasional MySQL. Sistem ini dirancang khusus untuk membantu operasional gudang dan toko "
            "skala kecil hingga menengah dalam mendata master barang, melacak supplier dan kategori, mencatat setiap "
            "transaksi masuk maupun keluar secara otomatis, serta memberikan notifikasi peringatan dini apabila stok "
            "barang mencapai batas minimum."
        )
        ctk.CTkLabel(
            about_card,
            text=deskripsi_about,
            font=ctk.CTkFont(size=14),
            wraplength=950,
            justify="left"
        ).pack(anchor="w", padx=30, pady=(0, 25))

        # 3. Kartu Fitur Utama (3 Kolom)
        fitur_frame = ctk.CTkFrame(scroll_area, fg_color="transparent")
        fitur_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        fitur_frame.grid_columnconfigure((0, 1, 2), weight=1)

        fitur_list = [
            ("📊 Monitoring Stok Real-Time", "Pantau jumlah unit tersedia, harga beli, dan harga jual setiap barang dalam satu dashboard terpusat."),
            ("⚠️ Smart Low-Stock Alert", "Sistem otomatis mendeteksi dan menandai barang yang stoknya menyentuh batas minimum agar segera di-restock."),
            ("📜 Audit Log Transaksi", "Setiap mutasi barang masuk dan keluar tercatat lengkap beserta waktu transaksi dan nama petugas yang bertugas.")
        ]

        for idx, (judul, ket) in enumerate(fitur_list):
            card = ctk.CTkFrame(fitur_frame, corner_radius=12)
            card.grid(row=0, column=idx, sticky="nsew", padx=8)
            ctk.CTkLabel(card, text=judul, font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=20, pady=(20, 8))
            ctk.CTkLabel(card, text=ket, font=ctk.CTkFont(size=13), wraplength=280, justify="left").pack(anchor="w", padx=20, pady=(0, 20))

    def buat_footer(self):
        footer = ctk.CTkFrame(self, height=65, corner_radius=0)
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            footer,
            text="© 2026 Inventaris Pro System • D4 Teknologi Rekayasa Komputer - Polines",
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=0, padx=30, pady=20, sticky="w")

        ig_frame = ctk.CTkFrame(footer, fg_color="transparent")
        ig_frame.grid(row=0, column=2, padx=30, pady=15, sticky="e")

        ctk.CTkLabel(ig_frame, text="Follow Instagram Tim Kami:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(0, 10))

        # daftar team ig
        daftar_ig = [
            ("@nafi.munajib", "https://www.instagram.com/n4fi.m/"),
            ("@anggota_tim2", ""),
            ("@anggota_tim3", "")
        ]

        for username_ig, link_ig in daftar_ig:
            btn_ig = ctk.CTkButton(
                ig_frame,
                text=f"📷 {username_ig}",
                width=115,
                height=28,
                corner_radius=14,
                fg_color="#E1306C",
                hover_color="#C13584",
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda url=link_ig: webbrowser.open(url)
            )
            btn_ig.pack(side="left", padx=4)