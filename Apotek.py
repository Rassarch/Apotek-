import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Membuat/terhubung ke database
conn = sqlite3.connect('apotek.db')
cursor = conn.cursor()

# Membuat tabel jika belum ada
def create_tables():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS obat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        kategori TEXT NOT NULL,
        harga REAL NOT NULL,
        stok INTEGER NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transaksi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tanggal TEXT NOT NULL,
        total REAL NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transaksi_detail (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaksi_id INTEGER NOT NULL,
        obat_id INTEGER NOT NULL,
        jumlah INTEGER NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY(transaksi_id) REFERENCES transaksi(id),
        FOREIGN KEY(obat_id) REFERENCES obat(id)
    )
    ''')
    conn.commit()

# Fungsi untuk melayani pembeli
def melayani_pembeli():
    def tambah_obat_ke_keranjang():
        try:
            obat_id = int(entry_id_obat.get())
            jumlah = int(entry_jumlah.get())
            
            cursor.execute("SELECT nama, harga, stok FROM obat WHERE id = ?", (obat_id,))
            obat = cursor.fetchone()
            
            if obat:
                nama, harga, stok = obat
                if jumlah > stok:
                    messagebox.showerror("Error", f"Stok {nama} tidak mencukupi!")
                else:
                    subtotal = jumlah * harga
                    keranjang.append((obat_id, nama, jumlah, harga, subtotal))
                    update_keranjang()
            else:
                messagebox.showerror("Error", "ID obat tidak ditemukan!")
        except ValueError:
            messagebox.showerror("Error", "Masukkan data yang valid!")
    
    def update_keranjang():
        for item in tree_keranjang.get_children():
            tree_keranjang.delete(item)
        
        total = 0
        for idx, (obat_id, nama, jumlah, harga, subtotal) in enumerate(keranjang, start=1):
            total += subtotal
            tree_keranjang.insert('', 'end', values=(idx, nama, jumlah, harga, subtotal))
        
        label_total.config(text=f"Total: Rp {total:,.2f}")
        return total
    
    def selesaikan_transaksi():
        if not keranjang:
            messagebox.showerror("Error", "Keranjang kosong!")
            return
        
        total = update_keranjang()
        cursor.execute("INSERT INTO transaksi (tanggal, total) VALUES (datetime('now'), ?)", (total,))
        transaksi_id = cursor.lastrowid
        
        for obat_id, nama, jumlah, harga, subtotal in keranjang:
            cursor.execute("INSERT INTO transaksi_detail (transaksi_id, obat_id, jumlah, subtotal) VALUES (?, ?, ?, ?)",
                           (transaksi_id, obat_id, jumlah, subtotal))
            cursor.execute("UPDATE obat SET stok = stok - ? WHERE id = ?", (jumlah, obat_id))
        
        conn.commit()
        messagebox.showinfo("Sukses", f"Transaksi selesai! Total: Rp {total:,.2f}")
        keranjang.clear()
        update_keranjang()

    # Membuat window untuk melayani pembeli
    window = tk.Toplevel(root)
    window.title("Layanan Pembeli")
    
    tk.Label(window, text="ID Obat:").grid(row=0, column=0, padx=5, pady=5)
    entry_id_obat = tk.Entry(window)
    entry_id_obat.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(window, text="Jumlah:").grid(row=1, column=0, padx=5, pady=5)
    entry_jumlah = tk.Entry(window)
    entry_jumlah.grid(row=1, column=1, padx=5, pady=5)
    
    btn_tambah = tk.Button(window, text="Tambah ke Keranjang", command=tambah_obat_ke_keranjang)
    btn_tambah.grid(row=2, column=0, columnspan=2, pady=5)
    
    tree_keranjang = ttk.Treeview(window, columns=("No", "Nama Obat", "Jumlah", "Harga", "Subtotal"), show='headings')
    tree_keranjang.heading("No", text="No")
    tree_keranjang.heading("Nama Obat", text="Nama Obat")
    tree_keranjang.heading("Jumlah", text="Jumlah")
    tree_keranjang.heading("Harga", text="Harga")
    tree_keranjang.heading("Subtotal", text="Subtotal")
    tree_keranjang.grid(row=3, column=0, columnspan=2, pady=5)
    
    label_total = tk.Label(window, text="Total: Rp 0.00")
    label_total.grid(row=4, column=0, columnspan=2, pady=5)
    
    btn_selesai = tk.Button(window, text="Selesaikan Transaksi", command=selesaikan_transaksi)
    btn_selesai.grid(row=5, column=0, columnspan=2, pady=5)

# Fungsi untuk menampilkan menu utama
def menu_utama():
    btn_pembeli = tk.Button(root, text="Layani Pembeli", command=melayani_pembeli)
    btn_pembeli.pack(pady=10)
    
    btn_keluar = tk.Button(root, text="Keluar", command=root.destroy)
    btn_keluar.pack(pady=10)

# Inisialisasi Tkinter dan keranjang
create_tables()
root = tk.Tk()
root.title("Sistem Penjualan Apotek")
keranjang = []

menu_utama()
root.mainloop()
