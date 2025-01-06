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

# Fungsi untuk merekomendasikan obat berdasarkan keluhan
def rekomendasi_keluhan(keluhan):
    keluhan = keluhan.lower()

    # Daftar kata kunci dan rekomendasi obat
    rekomendasi = {
        'sakit kepala': "Paracetamol - Rp 5,000",
        'batuk': "Sirup Batuk ABC - Rp 12,000",
        'demam': "Ibuprofen - Rp 10,000",
        'flu': "Obat Flu XYZ - Rp 15,000",
        'nyeri': "Aspirin - Rp 7,500",
        'perut': "Antasida - Rp 8,000",
    }

    # Menentukan rekomendasi berdasarkan keluhan
    for keluhan_kata in rekomendasi:
        if keluhan_kata in keluhan:
            return rekomendasi[keluhan_kata]

    return "Maaf, kami tidak memiliki obat yang sesuai dengan keluhan Anda."

# Fungsi untuk melayani pembeli dengan chat responsif
def melayani_pembeli():
    keranjang = []
    
    print("\n*** Alif Farma - Layanan Pembeli ***")
    
    while True:
        print("\n1. Tambah Obat ke Keranjang")
        print("2. Selesaikan Transaksi")
        print("3. Chat Responsif (Keluhan)")
        print("4. Keluar")
        
        pilihan = input("Pilih menu (1/2/3/4): ")
        
        if pilihan == "1":
            try:
                obat_id = int(input("Masukkan ID Obat: "))
                jumlah = int(input("Masukkan Jumlah Obat: "))
                
                cursor.execute("SELECT nama, harga, stok FROM obat WHERE id = ?", (obat_id,))
                obat = cursor.fetchone()
                
                if obat:
                    nama, harga, stok = obat
                    if jumlah > stok:
                        print(f"Stok {nama} tidak mencukupi!")
                    else:
                        subtotal = jumlah * harga
                        keranjang.append((obat_id, nama, jumlah, harga, subtotal))
                        print(f"{nama} ditambahkan ke keranjang.")
                else:
                    print("ID obat tidak ditemukan!")
            except ValueError:
                print("Input tidak valid!")
        
        elif pilihan == "2":
            if not keranjang:
                print("Keranjang kosong!")
            else:
                total = sum(subtotal for _, _, _, _, subtotal in keranjang)
                cursor.execute("INSERT INTO transaksi (tanggal, total) VALUES (?, ?)", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total))
                transaksi_id = cursor.lastrowid
                
                for obat_id, nama, jumlah, harga, subtotal in keranjang:
                    cursor.execute("INSERT INTO transaksi_detail (transaksi_id, obat_id, jumlah, subtotal) VALUES (?, ?, ?, ?)",
                                   (transaksi_id, obat_id, jumlah, subtotal))
                    cursor.execute("UPDATE obat SET stok = stok - ? WHERE id = ?", (jumlah, obat_id))
                
                conn.commit()

                # Cetak struk
                waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("\n*** Alif Farma ***")
                print(f"Tanggal: {waktu}")
                print("=" * 30)
                print("{:<20}{:<5}{:<10}".format("Nama Obat", "Qty", "Subtotal"))
                for obat_id, nama, jumlah, harga, subtotal in keranjang:
                    print(f"{nama:<20}{jumlah:<5}Rp{subtotal:,.2f}")
                print("=" * 30)
                print(f"Total: Rp {total:,.2f}")
                print("=" * 30)
                print("Terima kasih telah berbelanja!")
                
                # Kosongkan keranjang setelah transaksi selesai
                keranjang.clear()

        elif pilihan == "3":
            keluhan = input("Masukkan keluhan Anda: ")
            rekomendasi = rekomendasi_keluhan(keluhan)
            print(f"Sistem: {rekomendasi}")
        
        elif pilihan == "4":
            print("Terima kasih telah menggunakan layanan kami.")
            break
        
        else:
            print("Pilihan tidak valid!")

# Inisialisasi dan mulai program
create_tables()
melayani_pembeli()

# Menutup koneksi ke database setelah program selesai
conn.close()
    
