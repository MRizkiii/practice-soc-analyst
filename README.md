# SOC Analyst - SSH Log Analyzer

Tools sederhana berbasis Python untuk menganalisis file log SSH (`auth.log`) guna mendeteksi aktivitas mencurigakan, seperti serangan Brute Force, serta memberikan statistik login.

### 1. Mode Web Dashboard (Tampilan Visual)

Jalankan perintah berikut(Pastikan menginstall Flask di environment dulu sebelum menjalankan perintah):

```bash
python app.py
```

Buka browser dan kunjungi `http://127.0.0.1:5000`. Anda akan melihat dashboard dengan tabel dan statistik.

### 2. Mode CLI (Terminal)

Jalankan perintah berikut:

```bash
python main.py
```

Hasil analisis akan langsung ditampilkan di terminal/console Anda.
