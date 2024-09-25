# Aplikasi URL Shortener

Aplikasi **URL Shortener** adalah aplikasi berbasis Python yang memungkinkan pengguna untuk memperpendek dan memperluas URL dengan cepat dan mudah. Aplikasi ini dilengkapi dengan fitur-fitur tambahan seperti pembuatan kode QR, riwayat penggunaan, auto-refresh URL, serta integrasi dengan clipboard dan browser.

## Fitur Utama
1. **Perpendek URL**: Menggunakan layanan TinyURL untuk memperpendek URL yang dimasukkan oleh pengguna.
2. **Perluas URL**: Memperluas URL yang telah diperpendek untuk mengembalikan ke URL aslinya.
3. **Salin URL**: Menyalin URL yang diperpendek langsung ke clipboard.
4. **Buka di Browser**: Membuka URL yang diperpendek di browser default.
5. **Pembuatan Kode QR**: Menghasilkan kode QR untuk URL yang dimasukkan, memudahkan pemindaian cepat.
6. **Riwayat URL**: Menyimpan dan menampilkan riwayat URL yang telah diperpendek.
7. **Ekspor Riwayat**: Ekspor riwayat URL yang telah diperpendek ke file teks.
8. **Auto-Refresh URL**: Memeriksa dan memperbarui URL secara otomatis setiap 60 detik.
9. **Pencarian Auto-Complete**: Masukkan URL lebih cepat dengan bantuan auto-complete dari riwayat URL.

## Instalasi

### Persyaratan
- Python 3.x
- Pustaka Python berikut:
  - `tkinter`
  - `pyshorteners`
  - `pyperclip`
  - `qrcode`
  - `validators`
  - `requests`
  - `PIL` (Untuk memproses gambar QR)
Untuk menginstal pustaka yang diperlukan, jalankan perintah berikut:
  ```bash
  pip install pyshorteners pyperclip qrcode[pil] validators requests
  ```

### Cara Menjalankan
1. Clone repositori ini dengan ``git clone https://github.com/Athallah1234/URL-Shortener.git``
2. Pastikan semua pustaka yang diperlukan telah diinstal dengan ``pip install -r requirements.txt``
3. Jalankan skrip menggunakan Python dengan ``python run.py``

### Penggunaan
1. **Perpendek URL**: Masukkan URL yang ingin diperpendek dan klik tombol **Shorten**.
2. **Perluas URL**: Masukkan URL pendek yang ingin diperluas dan klik tombol **Expand**.
3. **Salin URL**: Setelah URL diperpendek, klik tombol **Copy URL** untuk menyalin URL ke clipboard.
4. **Buka di Browser**: Klik tombol **Open in Browser** untuk membuka URL pendek di browser Anda.
5. **Buat Kode QR**: Masukkan URL pada bagian **Enter URL for QR Code** dan klik tombol **Generate QR Code** untuk membuat kode QR.
6. **Auto-Refresh URL**: Aktifkan opsi **Auto-Refresh URL** untuk memperbarui URL secara otomatis setiap 60 detik.
7. **Lihat Riwayat**: Klik tombol **Show History** untuk melihat URL yang telah diperpendek. Anda juga dapat menghapus atau mengekspor riwayat ke file teks.

### Log Aktivitas
Aplikasi ini menyimpan log aktivitas ke file url_shortener.log. Log ini mencatat setiap URL yang diperpendek, diperluas, disalin, dibuka di browser, atau ketika kode QR dibuat.

## FAQ
### 1. Apakah aplikasi ini bisa digunakan tanpa koneksi internet?
Tidak. Aplikasi ini bergantung pada layanan online untuk memperpendek URL, sehingga memerlukan koneksi internet.
### 2. Bagaimana saya bisa menambahkan layanan pemendek URL lain?
Anda bisa menambahkan layanan pemendek URL lain dengan memperluas penggunaan pustaka **PyShorteners**. Dokumentasi lengkap dapat ditemukan di [PyShorteners Docs](https://pyshorteners.readthedocs.io/).
### 3. Bagaimana cara mengatasi kesalahan 'Invalid URL'?
Pastikan URL yang dimasukkan adalah URL yang benar dengan format yang valid, misalnya dimulai dengan `http://` atau `https://`. Jika URL tersebut valid tetapi masih terjadi kesalahan, silakan coba ulang atau cek apakah layanan pemendek URL sedang mengalami masalah.

