import sqlite3

def hapus_data_akun():
    # Membuat koneksi ke database
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Menghapus semua data dari tabel akun
    c.execute('DELETE FROM akun;')

    # Commit perubahan dan menutup koneksi
    conn.commit()
    conn.close()

# Panggil fungsi untuk menghapus data
hapus_data_akun()
