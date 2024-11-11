import sqlite3

# Fungsi untuk membuat koneksi dan tabel di database SQLite
def create_db():
    conn = sqlite3.connect('data.db')  # Koneksi ke database
    c = conn.cursor()  # Membuat cursor untuk eksekusi query

    # Membuat tabel data_akuntansi (jurnal transaksi akuntansi) dengan default nilai upd_saldo 0
    c.execute('''CREATE TABLE IF NOT EXISTS data_akuntansi (
                    id INTEGER PRIMARY KEY,
                    tanggal TEXT,
                    no_produk TEXT,
                    no_akun TEXT,
                    keterangan TEXT,
                    debet REAL,
                    kredit REAL,
                    upd_saldo REAL DEFAULT 0)''')
    
    # Membuat tabel akun (nomor akun dan nama rekening)
    c.execute('''CREATE TABLE IF NOT EXISTS akun (
                    id_akun INTEGER PRIMARY KEY AUTOINCREMENT  ,
                    no_akun TEXT,
                    nama_rekening,
                    beban INTEGER)''')

    # Membuat tabel user (untuk login pengguna)
    c.execute('''CREATE TABLE IF NOT EXISTS user (
                    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    nama TEXT NOT NULL)''')

    # Commit perubahan dan menutup koneksi
    conn.commit()
    conn.close()

# Panggil fungsi untuk membuat tabel di database
create_db()
