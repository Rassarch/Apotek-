import json
import tkinter as tk
from tkinter import ttk, messagebox

# Fungsi untuk memuat data obat dari file JSON
def muat_data_obat(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Fungsi untuk menyimpan data obat ke file JSON
def simpan_data_obat(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Fungsi untuk menyimpan transaksi ke file JSON
def simpan_transaksi(file_path, transaksi):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    
    data.append(transaksi)
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Fungsi untuk menampilkan obat berdasarkan kategori dan subkategori
def tampilkan_obat(tree, data_obat, kategori, subkategori):
    tree.delete(*tree.get_children())
    if kategori in data_obat and subkategori in data_obat[kategori]:
        for obat in data_obat[kategori][subkategori]:
            tree.insert("", "end", values=(obat["id"], obat["nama"], f"Rp{obat['harga']:,}"))

# Fungsi utama untuk GUI
def apotek_ui(data_obat):
    keranjang = []

    def tambah_ke_keranjang():
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item, "values")
            jumlah = int(entry_jumlah.get() or 1)
            keranjang.append({"id": item[0], "nama": item[1], "harga": int(item[2][2:].replace(",", "")), "jumlah": jumlah})
            messagebox.showinfo("Keranjang", f"{jumlah} {item[1]} berhasil ditambahkan ke keranjang!")

    def tampilkan_keranjang():
        keranjang_window = tk.Toplevel(root)
        keranjang_window.title("Keranjang Belanja")
        keranjang_window.geometry("600x400")
        keranjang_window.resizable(False, False)

        frame_keranjang = ttk.Frame(keranjang_window, padding=10)
        frame_keranjang.pack(fill="both", expand=True)

        tree_keranjang = ttk.Treeview(frame_keranjang, columns=("ID", "Nama Obat", "Harga", "Jumlah"), show="headings", height=10)
        tree_keranjang.heading("ID", text="ID")
        tree_keranjang.heading("Nama Obat", text="Nama Obat")
        tree_keranjang.heading("Harga", text="Harga")
        tree_keranjang.heading("Jumlah", text="Jumlah")
        tree_keranjang.column("ID", width=50, anchor="center")
        tree_keranjang.column("Nama Obat", width=300)
        tree_keranjang.column("Harga", width=100, anchor="center")
        tree_keranjang.column("Jumlah", width=50, anchor="center")
        tree_keranjang.pack(fill="both", expand=True, side="left", padx=(0, 10))

        scrollbar = ttk.Scrollbar(frame_keranjang, orient="vertical", command=tree_keranjang.yview)
        tree_keranjang.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        def muat_keranjang():
            tree_keranjang.delete(*tree_keranjang.get_children())
            for item in keranjang:
                tree_keranjang.insert("", "end", values=(item["id"], item["nama"], f"Rp{item['harga']:,}", item["jumlah"]))

        def hapus_dari_keranjang():
            selected_item = tree_keranjang.selection()
            if selected_item:
                item = tree_keranjang.item(selected_item, "values")
                for i, obat in enumerate(keranjang):
                    if obat["id"] == item[0]:
                        keranjang.pop(i)
                        break
                muat_keranjang()
                messagebox.showinfo("Keranjang", f"{item[1]} berhasil dihapus dari keranjang!")

        def update_jumlah():
            selected_item = tree_keranjang.selection()
            if selected_item:
                item = tree_keranjang.item(selected_item, "values")
                new_jumlah = int(entry_jumlah_keranjang.get() or 1)
                for obat in keranjang:
                    if obat["id"] == item[0]:
                        obat["jumlah"] = new_jumlah
                        break
                muat_keranjang()
                messagebox.showinfo("Keranjang", f"Jumlah {item[1]} berhasil diupdate!")

        frame_control_keranjang = ttk.Frame(keranjang_window, padding=10)
        frame_control_keranjang.pack(fill="x")

        ttk.Label(frame_control_keranjang, text="Jumlah:", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_jumlah_keranjang = ttk.Entry(frame_control_keranjang, width=5)
        entry_jumlah_keranjang.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(frame_control_keranjang, text="Update Jumlah", command=update_jumlah).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Button(frame_control_keranjang, text="Hapus dari Keranjang", command=hapus_dari_keranjang).grid(row=0, column=3, padx=5, pady=5, sticky="w")

        muat_keranjang()

    def check_out():
        if not keranjang:
            messagebox.showwarning("Keranjang Kosong", "Keranjang belanja Anda kosong.")
            return

        total_harga = sum(item["jumlah"] * item["harga"] for item in keranjang)

        def lakukan_pembayaran():
            try:
                uang_diberikan = int(entry_uang.get())
                if uang_diberikan < total_harga:
                    messagebox.showwarning("Uang Kurang", "Uang yang diberikan kurang!")
                else:
                    kembalian = uang_diberikan - total_harga
                    transaksi = {
                        "total_harga": total_harga,
                        "uang_diberikan": uang_diberikan,
                        "kembalian": kembalian,
                        "items": keranjang
                    }
                    simpan_transaksi("transaksi.json", transaksi)
                    messagebox.showinfo("Pembayaran Berhasil", f"Total: Rp{total_harga:,}\nKembalian: Rp{kembalian:,}")
                    checkout_window.destroy()
                    keranjang.clear()
            except ValueError:
                messagebox.showerror("Input Error", "Masukkan jumlah uang yang valid!")

        checkout_window = tk.Toplevel(root)
        checkout_window.title("Check-out")
        checkout_window.geometry("300x200")
        checkout_window.resizable(False, False)

        frame_checkout = ttk.Frame(checkout_window, padding=20)
        frame_checkout.pack(fill="both", expand=True)

        ttk.Label(frame_checkout, text=f"Total: Rp{total_harga:,}", font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(frame_checkout, text="Masukkan Uang:", font=("Arial", 12)).pack(pady=5)
        entry_uang = ttk.Entry(frame_checkout)
        entry_uang.pack(pady=5)
        ttk.Button(frame_checkout, text="Bayar", command=lakukan_pembayaran).pack(pady=10)

    def pilih_kategori(event):
        subkategori_box["values"] = list(data_obat.get(kategori_box.get(), {}))
        subkategori_box.set("")

    def pilih_subkategori(event):
        tampilkan_obat(tree, data_obat, kategori_box.get(), subkategori_box.get())

    # Setup UI
    root = tk.Tk()
    root.title("Apotek Alif Farma")
    root.geometry("600x500")
    root.resizable(False, False)

    # Frame untuk filter
    frame_filter = ttk.Frame(root, padding=10)
    frame_filter.pack(fill="x")

    ttk.Label(frame_filter, text="Kategori:", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    kategori_box = ttk.Combobox(frame_filter, state="readonly", values=list(data_obat.keys()))
    kategori_box.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    kategori_box.bind("<<ComboboxSelected>>", pilih_kategori)

    ttk.Label(frame_filter, text="Subkategori:", font=("Arial", 11)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    subkategori_box = ttk.Combobox(frame_filter, state="readonly")
    subkategori_box.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    subkategori_box.bind("<<ComboboxSelected>>", pilih_subkategori)

    # Frame untuk tabel
    frame_table = ttk.Frame(root, padding=10)
    frame_table.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame_table, columns=("ID", "Nama Obat", "Harga"), show="headings", height=10)
    tree.heading("ID", text="ID")
    tree.heading("Nama Obat", text="Nama Obat")
    tree.heading("Harga", text="Harga")
    tree.column("ID", width=50, anchor="center")
    tree.column("Nama Obat", width=300)
    tree.column("Harga", width=100, anchor="center")
    tree.pack(fill="both", expand=True, side="left", padx=(0, 10))

    scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Frame untuk kontrol
    frame_control = ttk.Frame(root, padding=10)
    frame_control.pack(fill="x")

    ttk.Label(frame_control, text="Jumlah:", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_jumlah = ttk.Entry(frame_control, width=5)
    entry_jumlah.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    ttk.Button(frame_control, text="Tambah ke Keranjang", command=tambah_ke_keranjang).grid(row=0, column=2, padx=5, pady=5, sticky="w")
    ttk.Button(frame_control, text="Lihat Keranjang", command=tampilkan_keranjang).grid(row=0, column=3, padx=5, pady=5, sticky="w")
    ttk.Button(frame_control, text="Check-out", command=check_out).grid(row=0, column=4, padx=5, pady=5, sticky="w")

    root.mainloop()
# Data obat
data_obat = {
    "Batuk, Pilek & Flu": {
        "Batuk & Flu": [
            {"id": "B1", "nama": "Paracetamol 500mg", "harga": 5000},
            {"id": "B2", "nama": "Mixagrip Flu & Batuk", "harga": 15000},
            {"id": "B3", "nama": "Actifed Plus Cough Supressant Sirup 60 ml (Merah)", "harga": 70500},
            {"id": "B4", "nama": "Panadol Flu & Batuk 10 Kaplet", "harga": 20000},
            {"id": "B5", "nama": "OB Herbal 15 ml 10 Sachet", "harga": 50500},
        ],
        "Nasal Spray & Dekongestan": [
            {"id": "N1", "nama": "Otrivin Nasal Spray", "harga": 45000},
            {"id": "N2", "nama": "Afrin Nasal Spray", "harga": 30000},
            {"id": "N3", "nama": "Iliadin Dewasa 0.05% Nasal Spray 10 ml", "harga": 93600},
            {"id": "N4", "nama": "Bigroot Nose Hygiene Ultra Gentle Baby 50 ml", "harga": 152000},
            {"id": "N5", "nama": "Vicks Inhaler", "harga": 16000},
        ],
        "Balsem & Minyak Esensial": [
            {"id": "M1", "nama": "Zam Buk Ointment 8 g", "harga": 16300},
            {"id": "M2", "nama": "Plossa Inhaler & Roll On Eucalyptus 8 ml", "harga": 12000},
            {"id": "M3", "nama": "Freshcare Roll On Minyak Angin Strong (Hot) 10 ml", "harga": 16700},
            {"id": "M4", "nama": "Vicks Vaporub 10 g", "harga": 10500},
            {"id": "M5", "nama": "Vicks Vaporub 25 g", "harga": 24700},
            {"id": "M6", "nama": "Vicks Vaporub 50 g", "harga": 46800},
        ],
        "Untuk Bayi & Anak": [
            {"id": "A1", "nama": "Mucera Drops 15 ml", "harga": 56900},
            {"id": "A2", "nama": "Alco Drops 15 ml", "harga": 133800},
            {"id": "A3", "nama": "Rhinos Neo Drops 10 ml", "harga": 86600},
            {"id": "A4", "nama": "Mucos Drops 20 ml", "harga": 49600},
            {"id": "A5", "nama": "OBH Combi Anak Batuk Plus Flu Strawberry 60 ml", "harga": 19700},
            {"id": "A6", "nama": "Vicks Formula 44 Anak Sirup 54 ml", "harga": 23500},
            {"id": "A7", "nama": "Vicks Formula 44 Anak Sirup 27 ml", "harga": 12700},
            {"id": "A8", "nama": "Imboost Cough Kids Syrup 60 ml", "harga": 28600},
            {"id": "A9", "nama": "Bisolvon Solution 50 ml", "harga": 121500},
        ],
        "Perawatan Herbal": [
            {"id": "H1", "nama": "Obat Batuk Cap Ibu & Anak Sirup 75 ml", "harga": 37400},
            {"id": "H2", "nama": "Silex Sirup 100 ml", "harga": 80000},
            {"id": "H3", "nama": "Vaporin Inhalasi Liquid 10 Kapsul", "harga": 56000},
            {"id": "H4", "nama": "Tolak Angin Flu 5 Sachet", "harga": 24800},
            {"id": "H5", "nama": "Komix Herbal 15 ml 4 Botol", "harga": 14200},
            {"id": "H6", "nama": "Obat Batuk Cap Ibu & Anak Sirup 150 ml", "harga": 85000},
        ]
    },
    "Demam & Nyeri": {
        "Pereda Demam & Nyeri": [
            {"id": "P1", "nama": "Sumagesic 600 mg 4 Tablet", "harga": 3200},
            {"id": "P2", "nama": "Opistan 500 mg 10 Kaplet", "harga": 8700},
            {"id": "P3", "nama": "Pamol 500 mg 10 Tablet", "harga": 13200},
            {"id": "P4", "nama": "Voltadex 50 mg 10 Tablet", "harga": 3200},
            {"id": "P5", "nama": "Paracetamol 500 mg 10 Kaplet", "harga": 3900},
            {"id": "P6", "nama": "Panadol 500 mg 10 Kaplet", "harga": 12700},
            {"id": "P7", "nama": "Sanmol Forte 4 Tablet", "harga": 3100},
            {"id": "P8", "nama": "Buscopan Plus 4 Tablet", "harga": 27600},
            {"id": "P9", "nama": "Farsifen 400 mg 10 Tablet", "harga": 11500},
            {"id": "P10", "nama": "Panadol Extra 10 Kaplet", "harga": 13900},
            {"id": "P11", "nama": "Sanmol 500 mg 4 Tablet", "harga": 2600}
        ],
        "Untuk Bayi & Anak": [
            {"id": "A1", "nama": "Tempra Sirup Rasa Anggur 60 ml", "harga": 55400},
            {"id": "A2", "nama": "Praxion Forte Suspensi 60 ml", "harga": 40000},
            {"id": "A3", "nama": "Sanmol Sirup 60 ml", "harga": 23400},
            {"id": "A4", "nama": "Bye Bye Fever Anak 1 Lembar", "harga": 11300},
            {"id": "A5", "nama": "Ottopan Sirup 60 ml", "harga": 37900},
            {"id": "A6", "nama": "Pamol Sirup 60 ml", "harga": 20200},
            {"id": "A7", "nama": "Sanmol Drops 15 ml", "harga": 24500},
            {"id": "A8", "nama": "Tempra Forte Sirup Rasa Jeruk 60 ml", "harga": 61200},
        ],
        "Terapi Panas & Dingin": [
            {"id": "T1", "nama": "Bye Bye Fever Dewasa 3 Lembar", "harga": 40900},
            {"id": "T2", "nama": "Koolfever For Adult 1 Sachet", "harga": 10300},
            {"id": "T3", "nama": "Bye Bye Fever Dewasa 1 Lembar", "harga": 16700},
            {"id": "T4", "nama": "Mami Plester Kompres 1 Sachet", "harga": 12100},
        ]
    },
    "Masalah Pencernaan": {
        "Asam Lambung & GERD": [
            {"id": "G1", "nama": "Promag Suspensi 60 ml", "harga": 20500},
            {"id": "G2", "nama": "Lansoprazole 30 mg 10 Kapsul", "harga": 16500},            
            {"id": "G3", "nama": "Propepsa Suspensi 100 ml", "harga": 99900},
            {"id": "G4", "nama": "Omeprazole 20 mg 10 Kapsul", "harga": 6500},
            {"id": "G5", "nama": "Polysilane 8 Tablet", "harga": 10900},
            {"id": "G6", "nama": "Promag 10 Tablet", "harga": 9800},
        ],
        "Mual & Muntah": [
            {"id": "M1", "nama": "Gerdilium 10 mg 10 Kaplet", "harga": 65400},
            {"id": "M2", "nama": "Domperidone 10 mg 10 Tablet", "harga": 5900},
            {"id": "M3", "nama": "Vometa Suspensi 60 ml", "harga": 83300},
        ],
        "Diare": [
            {"id": "D1", "nama": "Entrostop 20 Tablet", "harga": 20900},
            {"id": "D2", "nama": "Oralit 200 4.1 g 1 Sachet", "harga": 1500},
            {"id": "D3", "nama": "Diapet 10 Tablet", "harga": 5900},
            {"id": "D4", "nama": "Diaget 10 Tablet", "harga": 40600},
            {"id": "D5", "nama": "Laperamide 2 mg 10 Tablet", "harga": 3500},
        ],
        "Infeksi Cacing": [
            {"id": "C1", "nama": "Combantrin 250 mg 2 Tablet", "harga": 22300},
            {"id": "C1", "nama": "Combantrin 250 mg 2 Tablet", "harga": 22300},
            {"id": "C2", "nama": "Albendazole 400 mg 10 Tablet", "harga": 10900}
        ],
        "Sembelit & Wasir": [
            {"id": "W1", "nama": "Laxadine Emulsi 60 ml", "harga": 65500},
            {"id": "W2", "nama": "Ardium 500 mg 15 Tablet", "harga": 186000},
            {"id": "W3", "nama": "Opilax Sirup 60 ml", "harga": 85300}
        ]
    },
    "Alergi": {
        "Pereda Gatal": [
            {"id": "P1", "nama": "Caladine Lotion 60 ml", "harga": 21300},
            {"id": "P2", "nama": "Caladine Lotion 95 ml", "harga": 29800},
            {"id": "P3", "nama": "Herocyn Bedak Kulit 85 g", "harga": 16500}
        ]
    }
}

# Simpan data obat ke file JSON
simpan_data_obat("data_obat.json", data_obat)

# Jalankan antarmuka
apotek_ui(data_obat)
