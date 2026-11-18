import customtkinter as ctk
from landing_page import LandingPageFrame
from auth_ui import LoginFrame, RegisterFrame
from dashboard_ui import DashboardFrame

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Inventaris Pro System - Manajemen Stok Barang")
        self.geometry("1180x700")
        self.minsize(1020, 620)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_frame = None

        # Algoritma Alur Awal: Langsung menampilkan Landing Page
        self.tampilkan_landing()

    def ganti_halaman(self, frame_baru):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_baru
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def tampilkan_landing(self):
        frame = LandingPageFrame(
            master=self,
            on_login_click=self.tampilkan_login,
            on_register_click=self.tampilkan_register
        )
        self.ganti_halaman(frame)

    def tampilkan_login(self):
        frame = LoginFrame(
            master=self,
            on_login_success=self.tampilkan_dashboard,
            on_go_register=self.tampilkan_register,
            on_back_landing=self.tampilkan_landing
        )
        self.ganti_halaman(frame)

    def tampilkan_register(self):
        frame = RegisterFrame(
            master=self,
            on_go_login=self.tampilkan_login,
            on_back_landing=self.tampilkan_landing
        )
        self.ganti_halaman(frame)

    def tampilkan_dashboard(self, user_data):
        frame = DashboardFrame(
            master=self,
            user_data=user_data,
            on_logout=self.tampilkan_landing
        )
        self.ganti_halaman(frame)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()