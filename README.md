# scrap-bisnis-com
Scraping website Bisnis.com

Video Demo: https://drive.google.com/file/d/18eBp-sEqsyBqGqTftcs6NusXCZtX7sO5/view?usp=sharing

Ini adalah project untuk scraping artikel pada website Bisnis.com. Terdapat 2 mode yaitu Backtrack dan Standard:
1. Backtrack: Crawler dapat menerima parameter start date dan end date.
2. Standard: Crawler menjadi long running process mengambil artikel secara berkala.

## **Contoh hasil scraping dengan mode backtrack (range waktu)**
<img width="1630" height="776" alt="image" src="https://github.com/user-attachments/assets/bf54a0b7-4c9f-4119-b104-c929dcb787f7" />


<img width="1730" height="468" alt="image" src="https://github.com/user-attachments/assets/7877fd7a-db86-4981-9438-8cdbb86f6e92" />

## **Contoh hasil scraping dengan mode standard**
<img width="1444" height="590" alt="image" src="https://github.com/user-attachments/assets/9ec9446a-ca50-4b40-a911-75e11e737d55" />

## Arsitektur
* **`bisnis_crawler.py` (Modul Inti)**: Ini adalah jantung dari proyek. File ini berisi fungsi-fungsi esensial yang bertanggung jawab atas logika *crawling* dan *scraping*.
    * `fetch_articles_listing(page)`: Fungsi ini mengambil halaman daftar artikel dari `bisnis.com` untuk menemukan URL artikel.
    * `fetch_article(link)`: Fungsi ini menerima sebuah URL artikel, mengirimkan permintaan HTTP, lalu mem-parsing HTML untuk mengekstrak judul, konten, dan tanggal publikasi.
    * `backtrack(...)`: Fungsi ini mengatur logika *backtracking* dengan melakukan iterasi melalui halaman-halaman dan menyaring artikel berdasarkan rentang tanggal yang diberikan.

* **`backtrack.py` (Titik Masuk untuk Mode Backtrack)**: Sebuah antarmuka baris perintah (*command-line interface*) ringan yang mengimpor fungsi `backtrack` dari modul inti. Skrip ini menangani parsing argumen baris perintah (`start_date`, `end_date`) dan memulai proses *crawl*.

* **`standard.py` (Titik Masuk untuk Mode Standar)**: Skrip ini mengimplementasikan fitur pemantauan berkelanjutan. Skrip ini mengimpor fungsi-fungsi dari modul inti dan menjalankan *loop* tak terbatas yang secara berkala memanggil *crawler*, lalu menyimpan setiap artikel baru yang ditemukan.
 
## Cara Menjalankan

### 1. Mode Backtrack

Untuk mengumpulkan artikel dalam rentang tanggal tertentu, gunakan `backtrack.py`.

**Sintaks:**
```bash
python backtrack.py <start_date> <end_date> [output_file]
```
* `<start_date>`: Tanggal mulai dalam format `DD-MM-YYYY`.
* `<end_date>`: Tanggal akhir dalam format `DD-MM-YYYY`.
* `[output_file]`: (Opsional) Nama file JSON untuk output. Standarnya adalah `hasil.json`.

**Contoh:**
Untuk mengambil semua artikel yang diterbitkan antara 15 September 2025 dan 16 September 2025.
```bash
python backtrack.py 15-09-2025 16-09-2025 hasil_backtrack.json
```

### 2. Mode Standar

Untuk memantau artikel baru secara terus-menerus, gunakan `standard.py`.

**Sintaks:**
```bash
python standard.py [interval] [output_file]
```
* `[interval]`: (Opsional) Waktu tunggu antar pemeriksaan, dalam detik. Standarnya adalah `60`.
* `[output_file]`: (Opsional) Nama file JSON untuk output. Standarnya adalah `hasil_standard.json`.

**Contoh:**
Untuk memeriksa artikel baru setiap 5 menit (300 detik) dan menyimpannya ke `articles.json`:
```bash
python standard.py 300 articles.json
```
Untuk menghentikan proses, tekan `CTRL+C`. Skrip akan menutup array JSON dengan benar sebelum keluar.



