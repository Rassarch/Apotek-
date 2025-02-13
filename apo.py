import sqlite3
from datetime import datetime

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
        total REAL NOT NULL,
        uang_dibayar REAL NOT NULL,
        kembalian REAL NOT NULL
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

# Fungsi untuk menambahkan obat baru (Admin)
def tambah_obat():
    nama = input("Masukkan nama obat: ")
    kategori = input("Masukkan kategori obat: ")
    harga = float(input("Masukkan harga obat: "))
    stok = int(input("Masukkan stok obat: "))
    cursor.execute("INSERT INTO obat (nama, kategori, harga, stok) VALUES (?, ?, ?, ?)", (nama, kategori, harga, stok))
    conn.commit()
    print("Obat berhasil ditambahkan!")

# Fungsi untuk menampilkan daftar obat
def tampilkan_obat():
    cursor.execute("SELECT * FROM obat")
    hasil = cursor.fetchall()
    print("Daftar Obat:")
    print("{:<5} {:<20} {:<15} {:<10} {:<5}".format("ID", "Nama", "Kategori", "Harga", "Stok"))
    for row in hasil:
        print("{:<5} {:<20} {:<15} {:<10} {:<5}".format(row[0], row[1], row[2], row[3], row[4]))

# Fungsi untuk melakukan transaksi (User)
def transaksi_penjualan():
    tampilkan_obat()
    id_transaksi = []
    total_harga = 0

    while True:
        obat_id = int(input("Masukkan ID obat (0 untuk selesai): "))
        if obat_id == 0:
            break
        jumlah = int(input("Masukkan jumlah: "))
        cursor.execute("SELECT nama, harga, stok FROM obat WHERE id = ?", (obat_id,))
        obat = cursor.fetchone()

        if obat:
            nama, harga, stok = obat
            if jumlah > stok:
                print(f"Stok tidak mencukupi untuk {nama}.")
            else:
                subtotal = jumlah * harga
                total_harga += subtotal
                id_transaksi.append((obat_id, jumlah, subtotal))
                cursor.execute("UPDATE obat SET stok = stok - ? WHERE id = ?", (jumlah, obat_id))
                print(f"Menambahkan {jumlah} x {nama} ke transaksi.")
        else:
            print("ID obat tidak ditemukan.")

    if id_transaksi:
        print(f"Total yang harus dibayar: Rp{total_harga:.2f}")
        uang_dibayar = float(input("Masukkan jumlah uang yang dibayarkan: "))
        if uang_dibayar < total_harga:
            print("Uang tidak cukup! Transaksi dibatalkan.")
            return
        kembalian = uang_dibayar - total_harga
        print(f"Kembalian: Rp{kembalian:.2f}")

        # Simpan transaksi
        cursor.execute("INSERT INTO transaksi (tanggal, total, uang_dibayar, kembalian) VALUES (?, ?, ?, ?)", ...),
        ((datetime.now(), total_harga, uang_dibayar, kembalian))
        transaksi_id = cursor.lastrowid

        for item in id_transaksi:
            obat_id, jumlah, subtotal = item
            cursor.execute("INSERT INTO transaksi_detail (transaksi_id, obat_id, jumlah, subtotal) VALUES (?, ?, ?, ?)",
                        (transaksi_id, obat_id, jumlah, subtotal))
        conn.commit()
        print("Transaksi selesai.")

# Fungsi untuk melihat riwayat transaksi (User)
def riwayat_transaksi():
    cursor.execute("SELECT * FROM transaksi")
    hasil = cursor.fetchall()
    print("Riwayat Transaksi:")
    print("{:<5} {:<20} {:<10} {:<10} {:<10}".format("ID", "Tanggal", "Total", "Dibayar", "Kembalian"))
    for row in hasil:
        print("{:<5} {:<20} {:<10} {:<10} {:<10}".format(row[0], row[1], row[2], row[3], row[4]))

# Menu Admin
def menu_admin():
    while True:
        print("\n=== Menu Admin ===")
        print("1. Tambah Obat")
        print("2. Tampilkan Obat")
        print("3. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            tambah_obat()
        elif pilihan == '2':
            tampilkan_obat()
        elif pilihan == '3':
            break
        else:
            print("Pilihan tidak valid!")

# Menu User
def menu_user():
    while True:
        print("\n=== Menu User ===")
        print("1. Lakukan Transaksi")
        print("2. Lihat Riwayat Transaksi")
        print("3. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            transaksi_penjualan()
        elif pilihan == '2':
            riwayat_transaksi()
        elif pilihan == '3':
            break
        else:
            print("Pilihan tidak valid!")

# Menu Utama
def menu():
    while True:
        print("\n=== Sistem Penjualan Apotek ===")
        print("1. Admin")
        print("2. User")
        print("3. Keluar")
        pilihan = input("Pilih peran: ")

        if pilihan == '1':
            menu_admin()
        elif pilihan == '2':
            menu_user()
        elif pilihan == '3':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid!")

# Menjalankan program
if __name__ == "__main__":
    create_tables()
    menu()
