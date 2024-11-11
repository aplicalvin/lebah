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
        beban_display = "Yes" if row[3] == 1 else "No"
        tree.insert("", "end", values=(row[0], row[1], row[2], beban_display))

# Fungsi untuk membuat form tambah/edit akun dalam popup
def popup_akun(action, tree, id_akun=None, no_akun=None, nama_rekening=None, beban=None):
    def submit_akun():
        no_akun = entry_no_akun.get()
        nama_rekening = entry_nama_rekening.get()
        beban = beban_var.get()  # Ambil nilai beban (0 atau 1)
        if no_akun and nama_rekening:
            if action == "tambah":
                tambah_akun(no_akun, nama_rekening, beban)
            elif action == "edit":
                edit_akun(id_akun, no_akun, nama_rekening, beban)
            tampilkan_akun(tree)
            popup.destroy()
        else:
            messagebox.showerror("Error", "Semua kolom harus diisi")

    popup = tk.Toplevel()
    popup.title("Tambah/Edit Akun")
    popup.geometry("300x250")

    tk.Label(popup, text="No Akun:").grid(row=0, column=0)
    entry_no_akun = tk.Entry(popup)
    entry_no_akun.grid(row=0, column=1)
    if no_akun:
        entry_no_akun.insert(0, no_akun)

    tk.Label(popup, text="Nama Rekening:").grid(row=1, column=0)
    entry_nama_rekening = tk.Entry(popup)
    entry_nama_rekening.grid(row=1, column=1)
    if nama_rekening:
        entry_nama_rekening.insert(0, nama_rekening)

    beban_var = tk.IntVar()
    beban_var.set(beban if beban is not None else 0)

    tk.Label(popup, text="Apakah Beban?").grid(row=2, column=0)
    radio_no = tk.Radiobutton(popup, text="No", variable=beban_var, value=0)
    radio_no.grid(row=2, column=1)
    radio_yes = tk.Radiobutton(popup, text="Yes", variable=beban_var, value=1)
    radio_yes.grid(row=2, column=2)

    submit_button = tk.Button(popup, text="Simpan", command=submit_akun)
    submit_button.grid(row=3, columnspan=2, pady=10)

# Fungsi untuk menghapus akun melalui konfirmasi
def confirm_hapus_akun(tree):
    selected_item = tree.selection()
    if selected_item:
        id_akun = tree.item(selected_item)["values"][0]
        result = messagebox.askyesno("Konfirmasi Hapus", "Apakah Anda yakin ingin menghapus akun ini?")
        if result:
            hapus_akun(id_akun)
            tampilkan_akun(tree)
    else:
        messagebox.showerror("Error", "Pilih akun yang ingin dihapus")

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

# Fungsi untuk membuat form tambah/edit user dalam popup
def popup_user(action, tree, id_user=None, username=None, password=None, nama=None):
    def submit_user():
        username = entry_username.get()
        password = entry_password.get()
        nama = entry_nama_user.get()
        if username and password and nama:
            if action == "tambah":
                tambah_user(username, password, nama)
            elif action == "edit":
                edit_user(id_user, username, password, nama)
            tampilkan_user(tree)
            popup.destroy()
        else:
            messagebox.showerror("Error", "Semua kolom harus diisi")

    popup = tk.Toplevel()
    popup.title("Tambah/Edit User")
    popup.geometry("300x250")

    tk.Label(popup, text="Username:").grid(row=0, column=0)
    entry_username = tk.Entry(popup)
    entry_username.grid(row=0, column=1)
    if username:
        entry_username.insert(0, username)

    tk.Label(popup, text="Password:").grid(row=1, column=0)
    entry_password = tk.Entry(popup, show="*")
    entry_password.grid(row=1, column=1)
    if password:
        entry_password.insert(0, password)

    tk.Label(popup, text="Nama:").grid(row=2, column=0)
    entry_nama_user = tk.Entry(popup)
    entry_nama_user.grid(row=2, column=1)
    if nama:
        entry_nama_user.insert(0, nama)

    submit_button = tk.Button(popup, text="Simpan", command=submit_user)
    submit_button.grid(row=3, columnspan=2, pady=10)

# Fungsi untuk menghapus user melalui konfirmasi
def confirm_hapus_user(tree):
    selected_item = tree.selection()
    if selected_item:
        id_user = tree.item(selected_item)["values"][0]
        result = messagebox.askyesno("Konfirmasi Hapus", "Apakah Anda yakin ingin menghapus user ini?")
        if result:
            hapus_user(id_user)
            tampilkan_user(tree)
    else:
        messagebox.showerror("Error", "Pilih user yang ingin dihapus")

# Fungsi untuk membuat halaman utama dan menu CRUD
def create_page(parent):
    header = tk.Label(parent, text="Pengaturan", font=("Arial", 18), bg="sky blue", anchor="w", padx=20)
    header.pack(fill="x", pady=10)

    tab_control = ttk.Notebook(parent)
    tab_akun = ttk.Frame(tab_control)
    tab_user = ttk.Frame(tab_control)
    
    tab_control.add(tab_akun, text="Akun")
    tab_control.add(tab_user, text="User")
    tab_control.pack(expand=1, fill="both")

    label_akun = tk.Label(tab_akun, text="Daftar Akun", font=("Arial", 14, "bold"))
    label_akun.pack(pady=10)

    columns = ("ID Akun", "No Akun", "Nama Rekening", "Beban")
    tree_akun = ttk.Treeview(tab_akun, columns=columns, show="headings")
    for col in columns:
        tree_akun.heading(col, text=col)
    tree_akun.pack(pady=10)
    tampilkan_akun(tree_akun)

    button_add_akun = tk.Button(tab_akun, text="Tambah Akun", command=lambda: popup_akun("tambah", tree_akun))
    button_add_akun.pack(pady=5)

    button_edit_akun = tk.Button(tab_akun, text="Edit Akun", command=lambda: popup_akun("edit", tree_akun, *tree_akun.item(tree_akun.selection())["values"]))
    button_edit_akun.pack(pady=5)

    button_delete_akun = tk.Button(tab_akun, text="Hapus Akun", command=lambda: confirm_hapus_akun(tree_akun))
    button_delete_akun.pack(pady=5)

    label_user = tk.Label(tab_user, text="Daftar User", font=("Arial", 14, "bold"))
    label_user.pack(pady=10)

    columns_user = ("ID User", "Username", "Password")
    tree_user = ttk.Treeview(tab_user, columns=columns_user, show="headings")
    for col in columns_user:
        tree_user.heading(col, text=col)
    tree_user.pack(pady=10)
    tampilkan_user(tree_user)

    button_add_user = tk.Button(tab_user, text="Tambah User", command=lambda: popup_user("tambah", tree_user))
    button_add_user.pack(pady=5)

    button_edit_user = tk.Button(tab_user, text="Edit User", command=lambda: popup_user("edit", tree_user, *tree_user.item(tree_user.selection())["values"]))
    button_edit_user.pack(pady=5)

    button_delete_user = tk.Button(tab_user, text="Hapus User", command=lambda: confirm_hapus_user(tree_user))
    button_delete_user.pack(pady=5)

# Fungsi untuk menjalankan aplikasi
def main():
    root = tk.Tk()
    root.title("Pengaturan Akun dan User")
    root.geometry("800x600")
    create_page(root)
    root.mainloop()

if __name__ == "__main__":
    main()
