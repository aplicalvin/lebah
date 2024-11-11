import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Fungsi untuk menambahkan akun
def tambah_akun(no_akun, nama_rekening, beban):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO akun (no_akun, nama_rekening, beban) VALUES (?, ?, ?)", (no_akun, nama_rekening, beban))
        conn.commit()
        messagebox.showinfo("Success", "Akun berhasil ditambahkan")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "No. Akun sudah ada")
    conn.close()

# Fungsi untuk mengedit akun
def edit_akun(id_akun, no_akun, nama_rekening, beban):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("UPDATE akun SET no_akun = ?, nama_rekening = ?, beban = ? WHERE id_akun = ?", (no_akun, nama_rekening, beban, id_akun))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Akun berhasil diperbarui")

# Fungsi untuk menghapus akun
def hapus_akun(id_akun):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("DELETE FROM akun WHERE id_akun = ?", (id_akun,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Akun berhasil dihapus")

# Fungsi untuk menampilkan data akun di Treeview
def tampilkan_akun(tree):
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM akun")
    rows = c.fetchall()
    conn.close()

    for row in rows:
        # Mengubah nilai beban 0 atau 1 menjadi Yes atau No
        beban_display = "Yes" if row[3] == 1 else "No"
        tree.insert("", "end", values=(row[0], row[1], row[2], beban_display))

# Fungsi untuk menambahkan user
def tambah_user(username, password, nama):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO user (username, password, nama) VALUES (?, ?, ?)", (username, password, nama))
        conn.commit()
        messagebox.showinfo("Success", "User berhasil ditambahkan")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username sudah ada")
    conn.close()

# Fungsi untuk mengedit user
def edit_user(id_user, username, password, nama):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("UPDATE user SET username = ?, password = ?, nama = ? WHERE id_user = ?", (username, password, nama, id_user))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "User berhasil diperbarui")

# Fungsi untuk menghapus user
def hapus_user(id_user):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("DELETE FROM user WHERE id_user = ?", (id_user,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "User berhasil dihapus")

# Fungsi untuk menampilkan data user di Treeview
def tampilkan_user(tree):
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user")
    rows = c.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", "end", values=row)

# Fungsi untuk membuat halaman utama dan menu CRUD
def create_page(parent):
    # Frame untuk judul
    header = tk.Label(parent, text="Pengaturan", font=("Arial", 18), bg="sky blue", anchor="w", padx=20)
    header.pack(fill="x", pady=10)

    # Tab untuk pengaturan akun dan user
    tab_control = ttk.Notebook(parent)
    tab_akun = ttk.Frame(tab_control)
    tab_user = ttk.Frame(tab_control)
    
    tab_control.add(tab_akun, text="Akun")
    tab_control.add(tab_user, text="User")
    tab_control.pack(expand=1, fill="both")

    # ==================================================================
    # Tabel dan CRUD untuk Akun
    label_akun = tk.Label(tab_akun, text="Daftar Akun", font=("Arial", 14, "bold"))
    label_akun.pack(pady=10)

    # Treeview untuk menampilkan akun
    columns = ("ID Akun", "No Akun", "Nama Rekening", "Beban")
    tree_akun = ttk.Treeview(tab_akun, columns=columns, show="headings")
    for col in columns:
        tree_akun.heading(col, text=col)
    tree_akun.pack(pady=10)
    tampilkan_akun(tree_akun)

    # Form untuk menambah/edit akun
    form_frame_akun = tk.Frame(tab_akun)
    form_frame_akun.pack(pady=10)

    tk.Label(form_frame_akun, text="No Akun:").grid(row=0, column=0)
    entry_no_akun = tk.Entry(form_frame_akun)
    entry_no_akun.grid(row=0, column=1)

    tk.Label(form_frame_akun, text="Nama Rekening:").grid(row=1, column=0)
    entry_nama_rekening = tk.Entry(form_frame_akun)
    entry_nama_rekening.grid(row=1, column=1)

    # Menambahkan pilihan Yes/No untuk 'beban'
    beban_var = tk.IntVar()  # Variabel untuk menampung nilai 0 atau 1
    beban_var.set(0)  # Defaultnya adalah No (beban = 0)

    tk.Label(form_frame_akun, text="Apakah Beban?").grid(row=2, column=0)
    radio_no = tk.Radiobutton(form_frame_akun, text="No", variable=beban_var, value=0)
    radio_no.grid(row=2, column=1)
    radio_yes = tk.Radiobutton(form_frame_akun, text="Yes", variable=beban_var, value=1)
    radio_yes.grid(row=2, column=2)

    def add_akun():
        no_akun = entry_no_akun.get()
        nama_rekening = entry_nama_rekening.get()
        beban = beban_var.get()  # Ambil nilai beban (0 atau 1)
        if no_akun and nama_rekening:
            tambah_akun(no_akun, nama_rekening, beban)
            tampilkan_akun(tree_akun)
        else:
            messagebox.showerror("Error", "Semua kolom harus diisi")

    def edit_akun_action():
        selected_item = tree_akun.selection()
        if selected_item:
            id_akun = tree_akun.item(selected_item)["values"][0]
            no_akun = entry_no_akun.get()
            nama_rekening = entry_nama_rekening.get()
            beban = beban_var.get()  # Ambil nilai beban (0 atau 1)
            if no_akun and nama_rekening:
                edit_akun(id_akun, no_akun, nama_rekening, beban)
                tampilkan_akun(tree_akun)
            else:
                messagebox.showerror("Error", "Semua kolom harus diisi")
        else:
            messagebox.showerror("Error", "Pilih akun yang ingin diedit")

    def delete_akun():
        selected_item = tree_akun.selection()
        if selected_item:
            id_akun = tree_akun.item(selected_item)["values"][0]
            hapus_akun(id_akun)
            tampilkan_akun(tree_akun)
        else:
            messagebox.showerror("Error", "Pilih akun yang ingin dihapus")

    # Tombol untuk CRUD Akun
    button_add_akun = tk.Button(tab_akun, text="Tambah Akun", command=add_akun)
    button_add_akun.pack(pady=5)

    button_edit_akun = tk.Button(tab_akun, text="Edit Akun", command=edit_akun_action)
    button_edit_akun.pack(pady=5)

    button_delete_akun = tk.Button(tab_akun, text="Hapus Akun", command=delete_akun)
    button_delete_akun.pack(pady=5)

    # ==================================================================
    # Tabel dan CRUD untuk User
    label_user = tk.Label(tab_user, text="Daftar User", font=("Arial", 14, "bold"))
    label_user.pack(pady=10)

    # Treeview untuk menampilkan user
    columns_user = ("ID User", "Username", "Password")
    tree_user = ttk.Treeview(tab_user, columns=columns_user, show="headings")
    for col in columns_user:
        tree_user.heading(col, text=col)
    tree_user.pack(pady=10)
    tampilkan_user(tree_user)

    # Form untuk menambah/edit user
    form_frame_user = tk.Frame(tab_user)
    form_frame_user.pack(pady=10)

    tk.Label(form_frame_user, text="Username:").grid(row=0, column=0)
    entry_username = tk.Entry(form_frame_user)
    entry_username.grid(row=0, column=1)

    tk.Label(form_frame_user, text="Password:").grid(row=1, column=0)
    entry_password = tk.Entry(form_frame_user, show="*")
    entry_password.grid(row=1, column=1)

    tk.Label(form_frame_user, text="Nama:").grid(row=2, column=0)
    entry_nama_user = tk.Entry(form_frame_user)
    entry_nama_user.grid(row=2, column=1)

    def add_user():
        username = entry_username.get()
        password = entry_password.get()
        nama = entry_nama_user.get()
        if username and password and nama:
            tambah_user(username, password, nama)
            tampilkan_user(tree_user)
        else:
            messagebox.showerror("Error", "Semua kolom harus diisi")

    def edit_user_action():
        selected_item = tree_user.selection()
        if selected_item:
            id_user = tree_user.item(selected_item)["values"][0]
            username = entry_username.get()
            password = entry_password.get()
            nama = entry_nama_user.get()
            if username and password and nama:
                edit_user(id_user, username, password, nama)
                tampilkan_user(tree_user)
            else:
                messagebox.showerror("Error", "Semua kolom harus diisi")
        else:
            messagebox.showerror("Error", "Pilih user yang ingin diedit")

    def delete_user():
        selected_item = tree_user.selection()
        if selected_item:
            id_user = tree_user.item(selected_item)["values"][0]
            hapus_user(id_user)
            tampilkan_user(tree_user)
        else:
            messagebox.showerror("Error", "Pilih user yang ingin dihapus")

    # Tombol untuk CRUD User
    button_add_user = tk.Button(tab_user, text="Tambah User", command=add_user)
    button_add_user.pack(pady=5)

    button_edit_user = tk.Button(tab_user, text="Edit User", command=edit_user_action)
    button_edit_user.pack(pady=5)

    button_delete_user = tk.Button(tab_user, text="Hapus User", command=delete_user)
    button_delete_user.pack(pady=5)

# Fungsi untuk menjalankan aplikasi
def main():
    create_db()  # Membuat database dan tabel jika belum ada
    root = tk.Tk()
    root.title("Pengaturan Akun dan User")
    root.geometry("800x600")
    create_page(root)
    root.mainloop()

if __name__ == "__main__":
    main()