# ==========================================
# 1. BAGIAN FILTERING (Menyaring Baris)
# ==========================================
def saring_log_sshd(daftar_log):
    ssh_log = []
    for baris in daftar_log:
        if 'sshd' in baris:
            ssh_log.append(baris)
    return ssh_log

# ==========================================
# 2. BAGIAN PARSING (Mengambil Data Spesifik)
# ==========================================
def ambil_data_dari_baris(x):
    hasil_satu_baris = []
    x = x.replace("  ", " ")
    pos = 0
    
    while True:
        Dfor = x.find("for ", pos)
        if Dfor == -1: break

        Auser = Dfor + 4
        Buser = x.find(" ", Auser)
        if Buser == -1: break
        
        if x[Auser:Buser] == "invalid":
            Auser = x.find("invalid user ") + 13
            Buser = x.find(" ", Auser)
            if Buser == -1: break   

        pos = Buser

        Dip = x.find("from ", pos)
        if Dip == -1: break
        Aip = Dip + 5
        Bip = x.find(" ", Aip)
        pos = Bip
        if Bip == -1: break

        Dport = x.find("port ", pos)
        if Dport == -1: break
        Aport = Dport + 5
        Bport = x.find(" ", Aport)
        if Bport == -1: break
        
        data = {
            "bulan" : x.split()[0],
            "jam" : x.split()[1],
            "tanggal" : x.split()[2],
            "user" : x[Auser:Buser],
            "ip" : x[Aip:Bip],
            "port" : x[Aport:Bport]
        }
        hasil_satu_baris.append(data)
    
    return hasil_satu_baris

# ==========================================
# 3. BAGIAN LOGIC (Alur Kerja Program)
# ==========================================

# Membaca File
with open("auth.log", "r") as f:
    logs = f.readlines()

# Menjalankan Fungsi Filtering
sshLog = saring_log_sshd(logs)

# Menjalankan Fungsi Parsing
fullData = []
for baris in sshLog:
    data_log = ambil_data_dari_baris(baris)
    # Memasukkan hasil parsing ke list utama
    for item in data_log:
        fullData.append(item)

# Menampilkan Hasil
print(fullData)