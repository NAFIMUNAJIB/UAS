import customtkinter as ctk
from tkinter import messagebox
from auth import login_user, register_user

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success, on_go_register, on_back_landing):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.on_login_success = on_login_success
        self.on_go_register = on_go_register
        self.on_back_landing = on_back_landing

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Top Bar Kembali
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=30, pady=20)
        ctk.CTkButton(
            top_bar, text="← Kembali ke Beranda", width=160, height=36,
            fg_color="transparent", border_width=1, text_color=("gray10", "gray90"),
            command=self.on_back_landing
        ).pack(side="left")

        # Card Form Login di Tengah
        card = ctk.CTkFrame(self, width=430, corner_radius=16)
        card.grid(row=1, column=0)
        card.grid_propagate(False)
        card.configure(height=470)

        ctk.CTkLabel(card, text="🔐 Login Petugas", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(35, 5))
        ctk.CTkLabel(card, text="Masuk untuk mengakses Dashboard Inventaris", font=ctk.CTkFont(size=13), text_color="gray").pack(pady=(0, 20))

        # Banner Pesan Error Spesifik
        self.error_label = ctk.CTkLabel(
            card, text="", font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ff4d4d", wraplength=350
        )
        self.error_label.pack(pady=(0, 8))

        # Input Username
        ctk.CTkLabel(card, text="Username", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=40)
        self.entry_user = ctk.CTkEntry(card, height=40, placeholder_text="Masukkan username Anda")
        self.entry_user.pack(fill="x", padx=40, pady=(4, 15))

        # Input Password
        ctk.CTkLabel(card, text="Password", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=40)
        self.entry_pass = ctk.CTkEntry(card, height=40, placeholder_text="Masukkan password Anda", show="*")
        self.entry_pass.pack(fill="x", padx=40, pady=(4, 8))

        # Checkbox Lihat Password
        self.show_pass_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            card, text="Tampilkan Password", variable=self.show_pass_var,
            font=ctk.CTkFont(size=12), command=self.toggle_password
        ).pack(anchor="w", padx=40, pady=(0, 20))

        # Tombol Masuk
        ctk.CTkButton(
            card, text="Masuk ke Dashboard", height=42,
            font=ctk.CTkFont(size=14, weight="bold"), command=self.proses_login
        ).pack(fill="x", padx=40, pady=(0, 15))

        # Link ke Register
        reg_frame = ctk.CTkFrame(card, fg_color="transparent")
        reg_frame.pack()
        ctk.CTkLabel(reg_frame, text="Belum punya akun?", font=ctk.CTkFont(size=12)).pack(side="left")
        ctk.CTkButton(
            reg_frame, text="Daftar Sekarang", width=100, height=24,
            fg_color="transparent", text_color="#3b8ed0", hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=12, weight="bold"), command=self.on_go_register
        ).pack(side="left")

    def toggle_password(self):
        self.entry_pass.configure(show="" if self.show_pass_var.get() else "*")

    def proses_login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        sukses, pesan, user_data = login_user(username, password)
        if sukses:
            self.error_label.configure(text="")
            messagebox.showinfo("Login Berhasil", pesan)
            self.on_login_success(user_data)
        else:
            # Menampilkan pesan error spesifik (misal: Username tidak terdaftar / Password salah)
            self.error_label.configure(text=f"⚠️ {pesan}")


class RegisterFrame(ctk.CTkFrame):
    def __init__(self, master, on_go_login, on_back_landing):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.on_go_login = on_go_login
        self.on_back_landing = on_back_landing

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Top Bar Kembali
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=30, pady=20)
        ctk.CTkButton(
            top_bar, text="← Kembali ke Beranda", width=160, height=36,
            fg_color="transparent", border_width=1, text_color=("gray10", "gray90"),
            command=self.on_back_landing
        ).pack(side="left")

        # Card Form Register
        card = ctk.CTkFrame(self, width=460, corner_radius=16)
        card.grid(row=1, column=0)
        card.grid_propagate(False)
        card.configure(height=560)

        ctk.CTkLabel(card, text="📝 Registrasi Akun Baru", font=ctk.CTkFont(size=23, weight="bold")).pack(pady=(28, 5))
        ctk.CTkLabel(card, text="Lengkapi data diri untuk membuat akun petugas", font=ctk.CTkFont(size=13), text_color="gray").pack(pady=(0, 15))

        self.error_label = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#ff4d4d", wraplength=380)
        self.error_label.pack(pady=(0, 5))

        # Field Input
        self.entry_nama = self.buat_input(card, "Nama Lengkap *", "Contoh: Nafi Munajib")
        self.entry_user = self.buat_input(card, "Username *", "Contoh: nafimunajib")
        self.entry_email = self.buat_input(card, "Email (Opsional)", "Contoh: nafi@polines.ac.id")
        self.entry_pass = self.buat_input(card, "Password *", "Buat password akun", is_pass=True)
        self.entry_konfirm = self.buat_input(card, "Konfirmasi Password *", "Ulangi password", is_pass=True)

        ctk.CTkButton(
            card, text="Daftar Akun", height=42, fg_color="#2fa572", hover_color="#248259",
            font=ctk.CTkFont(size=14, weight="bold"), command=self.proses_register
        ).pack(fill="x", padx=40, pady=(15, 12))

        login_frame = ctk.CTkFrame(card, fg_color="transparent")
        login_frame.pack()
        ctk.CTkLabel(login_frame, text="Sudah memiliki akun?", font=ctk.CTkFont(size=12)).pack(side="left")
        ctk.CTkButton(
            login_frame, text="Masuk di sini", width=90, height=24,
            fg_color="transparent", text_color="#3b8ed0", hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=12, weight="bold"), command=self.on_go_login
        ).pack(side="left")

    def buat_input(self, parent, label, placeholder, is_pass=False):
        ctk.CTkLabel(parent, text=label, font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=40)
        entry = ctk.CTkEntry(parent, height=36, placeholder_text=placeholder, show="*" if is_pass else "")
        entry.pack(fill="x", padx=40, pady=(2, 10))
        return entry

    def proses_register(self):
        nama = self.entry_nama.get().strip()
        user = self.entry_user.get().strip()
        email = self.entry_email.get().strip()
        pw = self.entry_pass.get().strip()
        konfirm = self.entry_konfirm.get().strip()

        if pw != konfirm:
            self.error_label.configure(text="⚠️ Konfirmasi password tidak cocok!")
            return

        sukses, pesan = register_user(nama, user, email, pw)
        if sukses:
            self.error_label.configure(text="")
            messagebox.showinfo("Registrasi Berhasil", pesan)
            # Otomatis diarahkan ke halaman Login setelah berhasil register
            self.on_go_login()
        else:
            self.error_label.configure(text=f"⚠️ {pesan}")