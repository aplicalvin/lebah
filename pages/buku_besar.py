import tkinter as tk
from tkinter import ttk
import sqlite3


# Fungsi untuk mengambil data berdasarkan No. Akun
def get_data_by_account(account_number):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM data_akuntansi WHERE no_akun = ?", (account_number,))
    data = c.fetchall()
    conn.close()
    return data

# Fungsi untuk menghitung total debit dan kredit per No. Akun
def hitung_total(data):
    total_debit = sum(row[5] for row in data)  # Kolom debet
    total_kredit = sum(row[6] for row in data)  # Kolom kredit
    return total_debit, total_kredit

# Fungsi untuk menampilkan data dalam tabel untuk setiap No. Akun
def tampilkan_data(tree_frame, account_number):
    # Hapus semua frame dan tabel yang lama
    for widget in tree_frame.winfo_children():
        widget.destroy()

    # Ambil data untuk No. Akun tertentu
    data = get_data_by_account(account_number)

    if not data:  # Jika tidak ada data untuk akun tersebut
        label_empty = tk.Label(tree_frame, text=f"Tidak ada data untuk No. Akun {account_number}")
        label_empty.pack()

    # Judul untuk tabel berdasarkan No. Akun
    label_account = tk.Label(tree_frame, text=f"Tabel untuk No. Akun {account_number}", font=("Arial", 14, "bold"))
    label_account.pack(pady=5)

    # Tabel untuk menampilkan data
    columns = ("Tanggal", "Keterangan", "Ref", "Debit", "Kredit", "Updt. Saldo")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(pady=10)

    # Hitung saldo berdasarkan transaksi
    saldo_terakhir = 0  # Misalnya saldo awal 0
    for row in data:
        # Menentukan debit dan kredit
        debit = row[5]
        kredit = row[6]

        # Hitung updt_saldo
        saldo_terakhir += debit  # Tambahkan saldo debit
        saldo_terakhir -= kredit  # Kurangi saldo kredit

        # Menampilkan data yang sesuai: Tanggal, Keterangan, Ref, Debit, Kredit, Saldo
        tree.insert('', 'end', values=(row[1], row[3], "JU", debit, kredit, saldo_terakhir))  # Menambahkan upd_saldo di kolom ke-6

    # Hitung total debit dan kredit
    total_debit, total_kredit = hitung_total(data)

    # Menampilkan total debit dan kredit di bawah tabel
    total_frame = tk.Frame(tree_frame)
    total_frame.pack(pady=5)

    label_total_debit = tk.Label(total_frame, text=f"Total Debit: {total_debit}")
    label_total_debit.grid(row=0, column=0, padx=10)

    label_total_kredit = tk.Label(total_frame, text=f"Total Kredit: {total_kredit}")
    label_total_kredit.grid(row=0, column=1, padx=10)

# Fungsi untuk mengambil semua No. Akun unik dari database
def get_unique_accounts():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT no_akun FROM data_akuntansi")
    accounts = c.fetchall()
    conn.close()
    return [account[0] for account in accounts]

# Fungsi untuk membuat halaman utama
def create_page(parent):
    # Frame untuk judul
    header = tk.Label(parent, text="Buku Besar", font=("Arial", 18), bg="sky blue", anchor="w", padx=20)
    header.pack(fill="x", pady=10)

    # Buat canvas dan scrollbar untuk menggulir seluruh halaman 
    canvas = tk.Canvas(parent)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Letakkan canvas dan scrollbar di frame
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Buat frame untuk menampung semua tabel dalam canvas
    page_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=page_frame, anchor="nw")

    # Ambil daftar No. Akun unik dari database
    accounts = get_unique_accounts()

    # Untuk setiap No. Akun, buat tabel dan tampilkan
    for account in accounts:
        account_frame = tk.Frame(page_frame)
        account_frame.pack(pady=10, fill="both", expand=True)

        # Menampilkan data untuk No. Akun tersebut
        tampilkan_data(account_frame, account)

    # Update scrollregion untuk canvas setelah semua data dimasukkan
    page_frame.update_idletasks()  # Update layout
    canvas.config(scrollregion=canvas.bbox("all"))  # Tentukan area yang dapat discroll
