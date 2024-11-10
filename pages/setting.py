import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Fungsi untuk menambahkan akun dengan id_akun berbasis timestamp
def tambah_akun(no_akun, nama_rekening, beban):
    # Generate id_akun dengan format yyyymmddhhmmss
    id_akun = datetime.now().strftime('%Y%m%d%H%M%S')  # Format: yyyymmddhhmmss
    
    # Koneksi ke database
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    try:
        # Menyisipkan data akun ke tabel akun dengan id_akun yang dihasilkan
        c.execute("INSERT INTO akun (id_akun, no_akun, nama_rekening, beban) VALUES (?, ?, ?, ?)", 
                  (id_akun, no_akun, nama_rekening, beban))
        conn.commit()  # Menyimpan perubahan
        messagebox.showinfo("Success", "Akun berhasil ditambahkan")
    except sqlite3.IntegrityError:
        # Menangani jika no_akun sudah ada (karena di database sudah diberi constraint UNIQUE)
        messagebox.showerror("Error", "No. Akun sudah ada")
    except Exception as e:
        # Menangani kesalahan lain
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
    finally:
        conn.close()  # Menutup koneksi

# Fungsi untuk menambahkan user dengan id_user berbasis timestamp
def tambah_user(username, password, nama):
    # Generate id_user dengan format yyyymmddhhmmss
    id_user = datetime.now().strftime('%Y%m%d%H%M%S')  # Format: yyyymmddhhmmss
    
    # Koneksi ke database
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    try:
        # Menyisipkan data user ke tabel user dengan id_user yang dihasilkan
        c.execute("INSERT INTO user (id_user, username, password, nama) VALUES (?, ?, ?, ?)", 
                  (id_user, username, password, nama))
        conn.commit()  # Menyimpan perubahan
        messagebox.showinfo("Success", "User berhasil ditambahkan")
    except sqlite3.IntegrityError:
        # Menangani jika username sudah ada (karena di database sudah diberi constraint UNIQUE)
        messagebox.showerror("Error", "Username sudah ada")
    except Exception as e:
        # Menangani kesalahan lain
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
    finally:
        conn.close()  # Menutup koneksi

# Fungsi untuk mengedit akun
def edit_akun(id_akun, no_akun, nama_rekening, beban):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("UPDATE akun SET no_akun = ?, nama_rekening = ?, beban = ? WHERE id_akun = ?", 
              (no_akun, nama_rekening, beban, id_akun))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Akun berhasil diperbarui")

# Fungsi untuk mengedit user
def edit_user(id_user, username, password, nama):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("UPDATE user SET username = ?, password = ?, nama = ? WHERE id_user = ?", 
              (username, password, nama, id_user))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "User berhasil diperbarui")

# Fungsi untuk menghapus akun
def hapus_akun(id_akun, tree):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("DELETE FROM akun WHERE id_akun = ?", (id_akun,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Akun berhasil dihapus")
    tampilkan_akun(tree)  # Refresh treeview setelah penghapusan

# Fungsi untuk menghapus user
def hapus_user(id_user, tree):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("DELETE FROM user WHERE id_user = ?", (id_user,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "User berhasil dihapus")
    tampilkan_user(tree)  # Refresh treeview setelah penghapusan

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
        tree.insert("", "end", values=(row[0], row[1], row[2]))

# Fungsi untuk menambah akun dengan form popup
def add_akun(tree):
    # Membuka jendela popup untuk memasukkan data akun baru
    add_window = tk.Toplevel()
    add_window.title("Tambah Akun")
    add_window.geometry("300x200")

    # Form untuk input akun baru
    tk.Label(add_window, text="No Akun:").grid(row=0, column=0)
    entry_no_akun = tk.Entry(add_window)
    entry_no_akun.grid(row=0, column=1)

    tk.Label(add_window, text="Nama Rekening:").grid(row=1, column=0)
    entry_nama_rekening = tk.Entry(add_window)
    entry_nama_rekening.grid(row=1, column=1)

    # Pilihan Beban (Yes/No)
    beban_var = tk.IntVar()
    beban_var.set(0)  # Default nilai beban No (0)

    tk.Label(add_window, text="Apakah Beban?").grid(row=2, column=0)
    radio_no = tk.Radiobutton(add_window, text="No", variable=beban_var, value=0)
    radio_no.grid(row=2, column=1)
    radio_yes = tk.Radiobutton(add_window, text="Yes", variable=beban_var, value=1)
    radio_yes.grid(row=2, column=2)

    # Fungsi untuk menyimpan data akun yang baru dimasukkan
    def save_akun():
        no_akun = entry_no_akun.get()
        nama_rekening = entry_nama_rekening.get()
        beban = beban_var.get()

        if no_akun and nama_rekening:  # Pastikan form tidak kosong
            # Menambahkan akun ke database
            tambah_akun(no_akun, nama_rekening, beban)
            tampilkan_akun(tree)  # Menampilkan ulang akun yang telah ditambahkan
            add_window.destroy()  # Menutup window popup
        else:
            messagebox.showerror("Error", "Semua kolom harus diisi")

    # Tombol untuk simpan akun
    tk.Button(add_window, text="Simpan", command=save_akun).grid(row=3, column=0, columnspan=2, pady=10)

# Fungsi untuk menambah user dengan form popup
def add_user(tree):
    # Membuka jendela popup untuk memasukkan data user baru
    add_window = tk.Toplevel()
    add_window.title("Tambah User")
    add_window.geometry("300x200")

    # Form untuk input user baru
    tk.Label(add_window, text="Username:").grid(row=0, column=0)
    entry_username = tk.Entry(add_window)
    entry_username.grid(row=0, column=1)

    tk.Label(add_window, text="Password:").grid(row=1, column=0)
    entry_password = tk.Entry(add_window, show="*")  # Password akan disembunyikan
    entry_password.grid(row=1, column=1)

    tk.Label(add_window, text="Nama:").grid(row=2, column=0)
    entry_nama = tk.Entry(add_window)
    entry_nama.grid(row=2, column=1)

    # Fungsi untuk menyimpan data user yang baru dimasukkan
    def save_user():
        username = entry_username.get()
        password = entry_password.get()
        nama = entry_nama.get()

        if username and password and nama:  # Pastikan form tidak kosong
            # Menambahkan user ke database
            tambah_user(username, password, nama)
            tampilkan_user(tree)  # Menampilkan ulang user yang telah ditambahkan
            add_window.destroy()  # Menutup window popup
        else:
            messagebox.showerror("Error", "Semua kolom harus diisi")

    # Tombol untuk simpan user
    tk.Button(add_window, text="Simpan", command=save_user).grid(row=3, column=0, columnspan=2, pady=10)

# Fungsi untuk menampilkan popup Edit User
def edit_user_popup(tree):
    selected_item = tree.selection()
    if selected_item:
        # Ambil ID user dari item yang dipilih
        id_user = tree.item(selected_item)["values"][0]
        username = tree.item(selected_item)["values"][1]
        nama = tree.item(selected_item)["values"][2]
        
        # Membuka popup untuk mengedit user
        edit_window = tk.Toplevel()
        edit_window.title("Edit User")
        edit_window.geometry("300x200")
        
        # Form untuk edit user
        tk.Label(edit_window, text="Username:").grid(row=0, column=0)
        entry_username = tk.Entry(edit_window)
        entry_username.insert(0, username)
        entry_username.grid(row=0, column=1)

        tk.Label(edit_window, text="Password:").grid(row=1, column=0)
        entry_password = tk.Entry(edit_window, show="*")  # Password akan disembunyikan
        entry_password.grid(row=1, column=1)

        tk.Label(edit_window, text="Nama:").grid(row=2, column=0)
        entry_nama = tk.Entry(edit_window)
        entry_nama.insert(0, nama)
        entry_nama.grid(row=2, column=1)

        def save_user():
            # Ambil nilai yang dimasukkan dalam form
            username = entry_username.get()
            password = entry_password.get()
            nama = entry_nama.get()

            if username and password and nama:
                # Update data user dengan id_user yang benar
                edit_user(id_user, username, password, nama)
                tampilkan_user(tree)  # Refresh treeview
                edit_window.destroy()  # Tutup popup
            else:
                messagebox.showerror("Error", "Semua kolom harus diisi")

        tk.Button(edit_window, text="Simpan", command=save_user).grid(row=3, column=0, columnspan=2, pady=10)

    else:
        messagebox.showerror("Error", "Pilih user yang ingin diedit")

# Fungsi untuk menghapus user dari tombol
def delete_user(tree):
    selected_item = tree.selection()
    if selected_item:
        id_user = tree.item(selected_item)["values"][0]
        hapus_user(id_user, tree)
    else:
        messagebox.showerror("Error", "Pilih user yang ingin dihapus")

# Fungsi untuk menghapus akun dari tombol
def delete_akun(tree):
    selected_item = tree.selection()
    if selected_item:
        id_akun = tree.item(selected_item)["values"][0]
        hapus_akun(id_akun, tree)
    else:
        messagebox.showerror("Error", "Pilih akun yang ingin dihapus")

# Membuat Tkinter Window
# root = tk.Tk()
# root.title("CRUD Aplikasi")

# Menambahkan tab untuk User dan Akun
tab_control = ttk.Notebook(root)

# Tab untuk Akun
tab_akun = ttk.Frame(tab_control)
tab_control.add(tab_akun, text='Akun')

# Treeview untuk menampilkan akun
tree_akun = ttk.Treeview(tab_akun, columns=("ID", "No. Akun", "Nama Rekening", "Beban"))
tree_akun.heading("#1", text="ID Akun")
tree_akun.heading("#2", text="No. Akun")
tree_akun.heading("#3", text="Nama Rekening")
tree_akun.heading("#4", text="Beban")
tree_akun.grid(row=0, column=0, columnspan=4)

# Tombol untuk menambah akun
tk.Button(tab_akun, text="Tambah Akun", command=lambda: add_akun(tree_akun)).grid(row=1, column=0)
tk.Button(tab_akun, text="Edit Akun", command=lambda: edit_akun_popup(tree_akun)).grid(row=1, column=1)
tk.Button(tab_akun, text="Hapus Akun", command=lambda: delete_akun(tree_akun)).grid(row=1, column=2)

# Tab untuk User
tab_user = ttk.Frame(tab_control)
tab_control.add(tab_user, text='User')

# Treeview untuk menampilkan user
tree_user = ttk.Treeview(tab_user, columns=("ID", "Username", "Nama"))
tree_user.heading("#1", text="ID User")
tree_user.heading("#2", text="Username")
tree_user.heading("#3", text="Nama")
tree_user.grid(row=0, column=0, columnspan=4)

# Tombol untuk menambah user
tk.Button(tab_user, text="Tambah User", command=lambda: add_user(tree_user)).grid(row=1, column=0)
tk.Button(tab_user, text="Edit User", command=lambda: edit_user_popup(tree_user)).grid(row=1, column=1)
tk.Button(tab_user, text="Hapus User", command=lambda: delete_user(tree_user)).grid(row=1, column=2)

tab_control.pack(expand=1, fill="both")

# Menampilkan data akun dan user
tampilkan_akun(tree_akun)
tampilkan_user(tree_user)

# Menjalankan aplikasi
# root.mainloop()
