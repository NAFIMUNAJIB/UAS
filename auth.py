import hashlib
from db_config import get_connection

def hash_password(password: str) -> str:
    """Mengubah password teks biasa menjadi hash SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register_user(nama_lengkap: str, username: str, email: str, password: str):
    """Mendaftarkan akun petugas baru ke tabel pengguna."""
    if not nama_lengkap or not username or not password:
        return False, "Nama Lengkap, Username, dan Password wajib diisi!"

    conn = get_connection()
    if not conn:
        return False, "Gagal terhubung ke database MySQL!"

    try:
        cursor = conn.cursor(dictionary=True)

        # 1. Cek apakah username sudah terdaftar
        cursor.execute("SELECT id_pengguna FROM pengguna WHERE username = %s", (username,))
        if cursor.fetchone():
            return False, f"Username '{username}' sudah terdaftar! Gunakan username lain."

        # 2. Cek email jika diisi (ubah string kosong menjadi None agar sesuai aturan UNIQUE MySQL)
        email_bersih = email.strip() if email.strip() else None
        if email_bersih:
            cursor.execute("SELECT id_pengguna FROM pengguna WHERE email = %s", (email_bersih,))
            if cursor.fetchone():
                return False, f"Email '{email_bersih}' sudah digunakan oleh akun lain!"

        # 3. Simpan data pengguna baru
        password_terenkripsi = hash_password(password)
        query = """
            INSERT INTO pengguna (nama_lengkap, username, email, password, peran, status_akun)
            VALUES (%s, %s, %s, %s, 'petugas', 'aktif')
        """
        cursor.execute(query, (nama_lengkap, username, email_bersih, password_terenkripsi))
        conn.commit()
        return True, "Registrasi berhasil! Silakan login menggunakan akun yang baru dibuat."

    except Exception as e:
        conn.rollback()
        return False, f"Terjadi kesalahan database: {e}"
    finally:
        cursor.close()
        conn.close()

def login_user(username: str, password: str):
    """Memvalidasi login pengguna dan memberikan pesan error spesifik jika gagal."""
    if not username or not password:
        return False, "Username dan Password tidak boleh kosong!", None

    conn = get_connection()
    if not conn:
        return False, "Gagal terhubung ke database MySQL!", None

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT id_pengguna, nama_lengkap, username, email, password, peran, status_akun 
            FROM pengguna 
            WHERE username = %s
        """
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        # 1. Validasi Username
        if not user:
            return False, "Username tidak terdaftar! Silakan periksa kembali atau daftar akun.", None

        # 2. Validasi Status Akun
        if user['status_akun'] != 'aktif':
            return False, "Akun Anda berstatus nonaktif. Hubungi administrator.", None

        # 3. Validasi Password (mendukung hash SHA-256 maupun password lama sebelum di-hash)
        password_input_hash = hash_password(password)
        if user['password'] != password_input_hash and user['password'] != password:
            return False, "Password salah! Silakan masukkan password yang benar.", None

        return True, f"Login berhasil! Selamat datang, {user['nama_lengkap']}.", user

    except Exception as e:
        return False, f"Terjadi kesalahan saat login: {e}", None
    finally:
        cursor.close()
        conn.close()