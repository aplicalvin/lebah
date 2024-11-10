import tkinter as tk
from tkinter import messagebox
import sqlite3
from navbar import create_sidebar  # Mengimpor sidebar/navbar dari navbar.py
from style import apply_styles

# Fungsi untuk memverifikasi username dan password
def verify_login(username, password):
    conn = sqlite3.connect('data.db')  # Koneksi ke database
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user  # Jika ditemukan, akan mengembalikan data user, jika tidak None

# Fungsi untuk membuat jendela login
def login_window():
    # Membuat jendela login
    login_win = tk.Tk()
    login_win.title("Login")
    login_win.geometry("400x250")

    # Label dan Entry untuk username
    tk.Label(login_win, text="Username").pack(pady=5)
    username_entry = tk.Entry(login_win, width=30)
    username_entry.pack(pady=5)

    # Label dan Entry untuk password
    tk.Label(login_win, text="Password").pack(pady=5)
    password_entry = tk.Entry(login_win, width=30, show="*")
    password_entry.pack(pady=5)

    # Fungsi untuk menangani login
    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        user = verify_login(username, password)
        if user:
            login_win.destroy()  # Menutup jendela login jika login berhasil
            open_main_window()  # Menjalankan aplikasi utama
        else:
            messagebox.showerror("Login Error", "Username atau Password salah")

    # Tombol untuk login
    tk.Button(login_win, text="Login", width=20, command=handle_login).pack(pady=20)

    login_win.mainloop()

# Fungsi untuk membuka aplikasi utama setelah login
def open_main_window():
    # GUI utama
    window = tk.Tk()
    window.title("Program Aplikasi Akuntansi")
    window.geometry("1280x720")

    # Terapkan styling dari file style.py
    apply_styles(window)

    # Frame utama untuk layout (menggunakan grid untuk lebih fleksibel)
    window.grid_rowconfigure(0, weight=1)  # Agar konten mengisi seluruh tinggi
    window.grid_columnconfigure(1, weight=1)  # Kolom konten utama memiliki bobot lebih besar

    # Frame konten utama (di kanan)
    frame_content = tk.Frame(window, bg="white")
    frame_content.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

    # Membuat sidebar di kiri
    current_page = "dashboard" 
    create_sidebar(window, frame_content, current_page)

    # Menambahkan header di bagian konten utama
    header = tk.Label(frame_content, text="Dashboard", font=("Arial", 18), bg="sky blue", anchor="w", padx=20)
    header.pack(fill="x", pady=10)

    # Menjalankan aplikasi
    window.mainloop()

# Menjalankan fungsi login saat aplikasi pertama kali dibuka
login_window()
