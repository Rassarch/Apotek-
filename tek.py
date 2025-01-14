import json
from datetime import datetime

# Nama file JSON untuk menyimpan data transaksi
FILE_TRANSAKSI = "transaksi.json"

# Fungsi untuk membuat atau membaca file transaksi JSON
def baca_file_transaksi():
    try:
        with open(FILE_TRANSAKSI, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Jika file tidak ada, buat file kosong
        return {}

def simpan_file_transaksi(data):
    with open(FILE_TRANSAKSI, "w") as file:
        json.dump(data, file, indent=4)

# Fungsi untuk menambahkan obat baru (hanya untuk admin)
def tambah_obat(obat_db):
    nama = input("Masukkan nama obat: ")
    kategori = input("Masukkan kategori obat: ")
    harga = float(input("Masukkan harga obat: "))
    stok = int(input("Masukkan stok obat: "))
    id_obat = len(obat_db) + 1
    obat_db[id_obat] = {
        "nama": nama,
        "kategori": kategori,
        "harga": harga,
        "stok": stok
    }
    print("Obat berhasil ditambahkan!")
    return obat_db

# Fungsi untuk menampilkan daftar obat
def tampilkan_obat(obat_db):
    print("\nDaftar Obat:")
    print("{:<5} {:<20} {:<15} {:<10} {:<5}".format("ID", "Nama", "Kategori", "Harga", "Stok"))
    for id_obat, detail in obat_db.items():
        print("{:<5} {:<20} {:<15} {:<10} {:<5}".format(
            id_obat, detail['nama'], detail['kategori'], detail['harga'], detail['stok']
        ))

# Fungsi transaksi untuk user
def transaksi_penjualan(obat_db):
    transaksi_data = baca_file_transaksi()
    pembeli_id = len(transaksi_data) + 1
    transaksi_data[pembeli_id] = {
        "tanggal": str(datetime.now()),
        "items": [],
        "total": 0,
        "uang_dibayar": 0,
        "kembalian": 0
    }
    total_harga = 0

    print("\n=== Transaksi Penjualan ===")
    tampilkan_obat(obat_db)

    while True:
        obat_id = int(input("Masukkan ID obat (0 untuk selesai): "))
        if obat_id == 0:
            break

        if obat_id not in obat_db:
            print("ID obat tidak ditemukan.")
            continue

        jumlah = int(input(f"Masukkan jumlah untuk {obat_db[obat_id]['nama']}: "))
        if jumlah > obat_db[obat_id]['stok']:
            print(f"Stok tidak mencukupi untuk {obat_db[obat_id]['nama']}.")
            continue

        subtotal = jumlah * obat_db[obat_id]['harga']
        total_harga += subtotal

        # Update stok obat
        obat_db[obat_id]['stok'] -= jumlah

        # Tambahkan item ke transaksi
        transaksi_data[pembeli_id]['items'].append({
            "id_obat": obat_id,
            "nama": obat_db[obat_id]['nama'],
            "jumlah": jumlah,
            "subtotal": subtotal
        })

    if total_harga > 0:
        print(f"\nTotal yang harus dibayar: {total_harga}")
        uang_dibayar = float(input("Masukkan jumlah uang yang dibayarkan: "))
        while uang_dibayar < total_harga:
            print("Uang yang dibayarkan tidak cukup!")
            uang_dibayar = float(input("Masukkan jumlah uang yang dibayarkan: "))

        kembalian = uang_dibayar - total_harga

        # Simpan total, uang dibayar, dan kembalian ke transaksi
        transaksi_data[pembeli_id]["total"] = total_harga
        transaksi_data[pembeli_id]["uang_dibayar"] = uang_dibayar
        transaksi_data[pembeli_id]["kembalian"] = kembalian

        simpan_file_transaksi(transaksi_data)
        print(f"Transaksi berhasil! Kembalian: {kembalian}")
    else:
        print("Transaksi dibatalkan.")

# Menu untuk admin
def menu_admin(obat_db):
    while True:
        print("\n=== Menu Admin ===")
        print("1. Tambah Obat")
        print("2. Tampilkan Obat")
        print("3. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            obat_db = tambah_obat(obat_db)
        elif pilihan == '2':
            tampilkan_obat(obat_db)
        elif pilihan == '3':
            break
        else:
            print("Pilihan tidak valid!")

    return obat_db

# Menu untuk user
def menu_user(obat_db):
    while True:
        print("\n=== Menu User ===")
        print("1. Lakukan Transaksi")
        print("2. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            transaksi_penjualan(obat_db)
        elif pilihan == '2':
            break
        else:
            print("Pilihan tidak valid!")

# Menu utama
def menu():
    # Database obat (berbasis dictionary)
    obat_db = {}

    while True:
        print("\n=== Sistem Penjualan Apotek ===")
        print("1. Admin")
        print("2. User")
        print("3. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            obat_db = menu_admin(obat_db)
        elif pilihan == '2':
            menu_user(obat_db)
        elif pilihan == '3':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid!")

# Menjalankan program
if __name__ == "__main__":
    menu()
    
