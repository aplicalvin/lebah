import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import sqlite3
from datetime import datetime

# Fungsi untuk menambah data ke database
def tambah_data(tanggal, no_produk, no_akun, keterangan, debet, kredit):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Ambil saldo kumulatif dari semua transaksi yang ada di database
    c.execute("SELECT SUM(kredit) - SUM(debet) FROM data_akuntansi")
    saldo_total = c.fetchone()[0]  # Saldo kumulatif dari semua transaksi

    # Jika saldo_total None (belum ada transaksi sebelumnya), set saldo_total ke 0
    if saldo_total is None:
        saldo_total = 0

    # Update saldo berdasarkan debit atau kredit
    if debet > 0:
        saldo_total -= debet  # Kurangi saldo jika ada debit
    elif kredit > 0:
        saldo_total += kredit  # Tambah saldo jika ada kredit

    # Insert data transaksi baru ke database dengan saldo kumulatif terbaru
    c.execute("INSERT INTO data_akuntansi (tanggal, no_produk, no_akun, keterangan, debet, kredit, upd_saldo) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (tanggal, no_produk, no_akun, keterangan, debet, kredit, saldo_total))

    conn.commit()
    conn.close()

# Fungsi untuk mengambil semua data dari database
def get_all_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM data_akuntansi")
    data = c.fetchall()
    conn.close()
    return data

# Fungsi untuk menghitung total debit dan kredit
def hitung_total():
    data = get_all_data()
    total_debit = sum(row[5] for row in data)  # Kolom debet
    total_kredit = sum(row[6] for row in data)  # Kolom kredit
    return total_debit, total_kredit

# Fungsi untuk menampilkan data dalam tabel
def tampilkan_data(tree, label_total_debit, label_total_kredit):
    for row in tree.get_children():
        tree.delete(row)
    
    data = get_all_data()
    for row in data:
        tree.insert('', 'end', values=row[1:])  # Menampilkan semua data kecuali ID
    
    # Hitung total debit dan kredit
    total_debit, total_kredit = hitung_total()
    label_total_debit.config(text=f"Total Debit: {total_debit}")
    label_total_kredit.config(text=f"Total Kredit: {total_kredit}")

# Fungsi untuk membuka popup form input data
def popup_input_data(parent, tree, label_total_debit, label_total_kredit, action, selected_item=None):
    def simpan_data():
        tanggal = cal.get_date()
        no_produk = entry_no_produk.get()
        no_akun = entry_no_akun.get()
        keterangan = entry_keterangan.get()
        debet = entry_debet.get()
        kredit = entry_kredit.get()
        
        # Validasi input
        if not no_akun or not keterangan or (not debet and not kredit):
            messagebox.showerror("Error", "Semua kolom harus diisi dengan benar!")
            return

        # Jika no_produk kosong, kita set menjadi None atau string kosong
        if not no_produk:
            no_produk = None  # Atau bisa "" jika diinginkan
        
        # Atur debet dan kredit secara otomatis
        debet = float(debet) if debet else 0
        kredit = float(kredit) if kredit else 0
        if debet > 0:
            kredit = 0
        if kredit > 0:
            debet = 0
        
        if action == "tambah":
            # Simpan data baru
            tambah_data(tanggal, no_produk, no_akun, keterangan, debet, kredit)
        elif action == "edit":
            # Edit data yang sudah ada
            id_data = selected_item[0]
            edit_data(id_data, tanggal, no_produk, no_akun, keterangan, debet, kredit)
        
        tampilkan_data(tree, label_total_debit, label_total_kredit)  # Refresh tabel
        popup.destroy()
    
    # Popup untuk input data
    popup = tk.Toplevel(parent)
    popup.title("Tambah/Edit Data Akuntansi")
    
    tk.Label(popup, text="Tanggal:").grid(row=0, column=0)
    cal = Calendar(popup, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.grid(row=0, column=1)
    cal.selection_set(datetime.today().date())  # Memilih tanggal default (hari ini)
    
    tk.Label(popup, text="No. Produk:").grid(row=1, column=0)
    entry_no_produk = tk.Entry(popup)
    entry_no_produk.grid(row=1, column=1)
    if action == "edit" and selected_item:
        entry_no_produk.insert(0, selected_item[2])  # No Produk
    
    tk.Label(popup, text="No. Akun:").grid(row=2, column=0)
    entry_no_akun = tk.Entry(popup)
    entry_no_akun.grid(row=2, column=1)
    if action == "edit" and selected_item:
        entry_no_akun.insert(0, selected_item[3])  # No Akun
    
    tk.Label(popup, text="Keterangan:").grid(row=3, column=0)
    entry_keterangan = tk.Entry(popup)
    entry_keterangan.grid(row=3, column=1)
    if action == "edit" and selected_item:
        entry_keterangan.insert(0, selected_item[4])  # Keterangan
    
    tk.Label(popup, text="Debet:").grid(row=4, column=0)
    entry_debet = tk.Entry(popup)
    entry_debet.grid(row=4, column=1)
    if action == "edit" and selected_item:
        entry_debet.insert(0, selected_item[5])  # Debet
    
    tk.Label(popup, text="Kredit:").grid(row=5, column=0)
    entry_kredit = tk.Entry(popup)
    entry_kredit.grid(row=5, column=1)
    if action == "edit" and selected_item:
        entry_kredit.insert(0, selected_item[6])  # Kredit
    
    # Tombol untuk menyimpan data
    tk.Button(popup, text="Simpan", command=simpan_data).grid(row=6, columnspan=2)

# Fungsi untuk mengedit data transaksi
def edit_data(id_data, tanggal, no_produk, no_akun, keterangan, debet, kredit):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Hitung saldo total setelah perubahan
    c.execute("SELECT SUM(kredit) - SUM(debet) FROM data_akuntansi")
    saldo_total = c.fetchone()[0]  # Saldo kumulatif dari semua transaksi

    # Jika saldo_total None (belum ada transaksi sebelumnya), set saldo_total ke 0
    if saldo_total is None:
        saldo_total = 0

    if debet > 0:
        saldo_total -= debet  # Kurangi saldo jika ada debit
    elif kredit > 0:
        saldo_total += kredit  # Tambah saldo jika ada kredit

    c.execute("""
        UPDATE data_akuntansi
        SET tanggal = ?, no_produk = ?, no_akun = ?, keterangan = ?, debet = ?, kredit = ?, upd_saldo = ?
        WHERE id_data = ?
    """, (tanggal, no_produk, no_akun, keterangan, debet, kredit, saldo_total, id_data))
    conn.commit()
    conn.close()

# Fungsi untuk menghapus data transaksi
def hapus_data(id_data, tree, label_total_debit, label_total_kredit):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("DELETE FROM data_akuntansi WHERE id_data = ?", (id_data,))
    conn.commit()
    conn.close()

    # Refresh tabel dan update total debit dan kredit
    tampilkan_data(tree, label_total_debit, label_total_kredit)

# Fungsi untuk konfirmasi penghapusan data
def confirm_hapus_data(tree, label_total_debit, label_total_kredit):
    selected_item = tree.selection()
    if selected_item:
        id_data = tree.item(selected_item)["values"][0]  # Ambil ID data yang dipilih
        result = messagebox.askyesno("Konfirmasi Hapus", "Apakah Anda yakin ingin menghapus data ini?")
        if result:
            hapus_data(id_data, tree, label_total_debit, label_total_kredit)
    else:
        messagebox.showerror("Error", "Pilih data yang ingin dihapus terlebih dahulu!")

# Fungsi untuk membuat halaman utama
def create_page(parent):
    header = tk.Label(parent, text="Input Data Jurnal Umum", font=("Arial", 18), bg="sky blue", anchor="w", padx=20)
    header.pack(fill="x", pady=10)

    canvas = tk.Canvas(parent)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    page_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=page_frame, anchor="nw")

    frame_tambah_data = tk.Frame(page_frame)
    frame_tambah_data.pack(pady=10)
    tk.Button(frame_tambah_data, text="Tambah Data", command=lambda: popup_input_data(page_frame, tree, label_total_debit, label_total_kredit, "tambah")).pack(side="left", padx=5)
    tk.Button(frame_tambah_data, text="Reset Data", command=lambda: reset_data(tree, label_total_debit, label_total_kredit)).pack(side="left", padx=5)

    columns = ("Tanggal", "No. Produk", "No. Akun", "Keterangan", "Debet", "Kredit")
    tree = ttk.Treeview(page_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(pady=10)

    label_total_debit = tk.Label(page_frame, text="Total Debit: 0")
    label_total_debit.pack(pady=5)

    label_total_kredit = tk.Label(page_frame, text="Total Kredit: 0")
    label_total_kredit.pack(pady=5)

    # Tombol edit dan hapus data
    tk.Button(page_frame, text="Edit Data", command=lambda: popup_input_data(page_frame, tree, label_total_debit, label_total_kredit, "edit", tree.item(tree.selection())["values"])).pack(pady=5)
    tk.Button(page_frame, text="Hapus Data", command=lambda: confirm_hapus_data(tree, label_total_debit, label_total_kredit)).pack(pady=5)

    tampilkan_data(tree, label_total_debit, label_total_kredit)

    page_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
