# Information Retrieval System

Sistem temu kembali informasi berbasis Command-Line Interface (CLI)
menggunakan Python. Program ini memuat beberapa dataset, melakukan
preprocessing teks, membangun indeks menggunakan Whoosh, dan mencari
dokumen berdasarkan query pengguna. Hasil pencarian ditampilkan
berdasarkan skor cosine similarity.

## Fitur

-   Memuat dan mengindeks dokumen dari lima sumber dataset:
    -   `etd-usk`
    -   `etd-ugm`
    -   `kompas`
    -   `tempo`
    -   `mojok`
-   Preprocessing teks: case folding, tokenisasi, penghapusan stopword,
    dan lemmatization berbasis kamus sederhana.
-   Pembuatan indeks dokumen menggunakan Whoosh.
-   Representasi teks menggunakan Bag of Words (BoW) melalui
    `CountVectorizer`.
-   Pemeringkatan hasil menggunakan cosine similarity.
-   Menampilkan maksimal lima hasil pencarian.
-   Menu CLI untuk memuat dataset, mencari dokumen, melihat informasi
    dataset, melihat informasi indeks, dan keluar dari program.

## Teknologi yang Digunakan

-   Python
-   Whoosh
-   scikit-learn
-   pandas

## Struktur Folder

``` text
UTS_Penelusuran_Informasi/
├── dataset/
│   ├── etd-usk/
│   ├── etd-ugm/
│   ├── kompas/
│   ├── tempo/
│   └── mojok/
├── storage/
├── main.py
├── preprocessing.py
├── indexing.py
├── search_engine.py
├── requirements.txt
└── README.md
```

Folder `storage/` digunakan untuk menyimpan indeks Whoosh yang dibuat
program. Indeks dapat dibuat ulang melalui menu **Load & Index
Dataset**.

## Persyaratan

Pastikan Python sudah terpasang. Periksa instalasi Python melalui
terminal:

``` bash
python --version
```

Jika perintah `python` tidak tersedia di Windows, coba:

``` powershell
py --version
```

## Instalasi

1.  Clone repositori:

    ``` bash
    git clone https://github.com/fitri-hub/Information-Retrieval-System
    ```

2.  Masuk ke folder proyek:

    ``` bash
    cd UTS
    ```

3.  Instal dependensi:

    ``` bash
    python -m pip install -r requirements.txt
    ```

Jika belum memiliki file `requirements.txt`, buat file tersebut dengan
isi:

``` text
Whoosh
scikit-learn
pandas
```

## Menyiapkan Dataset

Letakkan dataset di dalam folder `dataset/`, sesuai sumbernya:

``` text
dataset/
├── etd-usk/
├── etd-ugm/
├── kompas/
├── tempo/
└── mojok/
```

Versi program saat ini membaca file `.txt`, `.md`, dan `.csv`. Untuk
file CSV, setiap baris diperlakukan sebagai satu dokumen dan nilai kolom
digabungkan menjadi isi dokumen.

**Catatan:** file PDF belum dibaca langsung oleh versi program ini. Jika
dataset yang tersedia berbentuk PDF, teks perlu dikonversi terlebih
dahulu ke format yang didukung atau program perlu dikembangkan dengan
pembaca PDF.

## Menjalankan Program

Jalankan perintah berikut dari folder proyek:

``` bash
python main.py
```

Di Windows, alternatifnya:

``` powershell
py main.py
```

Menu utama program:

``` text
==================================================
          INFORMATION RETRIEVAL SYSTEM
==================================================
Status Dataset : Belum dimuat
Status Index   : Belum tersedia
Jumlah Dokumen : 0
--------------------------------------------------
[1] Load & Index Dataset
[2] Search Query
[3] Show Dataset Information
[4] Show Index Information
[5] Exit
==================================================
Pilih menu (1-5):
```

### Cara Menggunakan

1.  Pilih menu `1` untuk memuat dataset dan membuat indeks Whoosh.
2.  Periksa jumlah dokumen yang berhasil dimuat dari setiap sumber.
3.  Pilih menu `2`, lalu masukkan kata atau kalimat yang ingin dicari.
4.  Baca hasil pencarian yang memuat peringkat, judul, sumber, skor, dan
    cuplikan isi dokumen.
5.  Pilih menu `3` untuk melihat jumlah dokumen per dataset.
6.  Pilih menu `4` untuk memeriksa status dan lokasi indeks.
7.  Pilih menu `5` untuk keluar dari program.

Dataset harus dimuat dan diindeks terlebih dahulu sebelum pencarian
dilakukan.

## Alur Sistem

1.  **Load dataset:** program membaca file yang didukung dari setiap
    folder dataset.
2.  **Preprocessing:** teks diubah menjadi huruf kecil, dipecah menjadi
    token, stopword dihapus, lalu kata yang ada di kamus lemmatization
    sederhana diubah ke bentuk dasar.
3.  **Indexing:** teks hasil preprocessing disimpan dalam indeks Whoosh.
4.  **Representasi BoW:** `CountVectorizer` mengubah dokumen dan query
    menjadi vektor berdasarkan frekuensi kata.
5.  **Pencarian:** Whoosh digunakan untuk menemukan dokumen yang cocok
    dengan query.
6.  **Pemeringkatan:** dokumen yang ditemukan diurutkan berdasarkan
    cosine similarity.
7.  **Menampilkan hasil:** program menampilkan maksimal lima dokumen
    dengan skor tertinggi.

## Catatan tentang Skor Pencarian

Cosine similarity mengukur kemiripan antara vektor query dan vektor
dokumen. Untuk representasi BoW yang digunakan program ini, skor yang
lebih tinggi menunjukkan pola kata yang lebih mirip. Skor ini tidak
selalu berarti bahwa dokumen paling relevan secara makna.

Pada implementasi saat ini, Whoosh terlebih dahulu menyaring dokumen
yang cocok, kemudian cosine similarity digunakan untuk mengurutkan
dokumen hasil penyaringan tersebut.

## Pemecahan Masalah

-   **Dataset tidak ditemukan:** pastikan folder `dataset/` berada
    sejajar dengan `main.py`.
-   **Jumlah dokumen nol:** pastikan file dataset menggunakan ekstensi
    `.txt`, `.md`, atau `.csv` dan berisi teks.
-   **Modul tidak ditemukan:** jalankan
    `python -m pip install -r requirements.txt`.
-   **Tidak ada hasil pencarian:** coba query lain yang kata-katanya
    terdapat di dalam dataset.
-   **Index belum tersedia:** jalankan program dan pilih menu `1`
    terlebih dahulu.

## Batasan

-   Format PDF belum didukung secara langsung.
-   Lemmatization menggunakan kamus sederhana sehingga tidak mencakup
    seluruh bentuk kata bahasa Indonesia.
-   Kualitas hasil pencarian bergantung pada isi dataset, preprocessing,
    query, dan kecocokan kata.
-   Dataset harus disediakan secara terpisah kecuali memang diizinkan
    untuk didistribusikan bersama repositori.

## Pengembangan Selanjutnya

-   Menambahkan dukungan pembacaan PDF jika diperbolehkan oleh ketentuan
    tugas.
-   Mengembangkan kamus atau metode stemming/lemmatization bahasa
    Indonesia.
-   Menampilkan cuplikan yang lebih relevan dengan query.
-   Menambahkan pengujian kualitas hasil pencarian.

## Kontributor

-   Anggota 1: Fitriani (2408107010022)
-   Anggota 2: Zahra Rizkyna (2408107010031)
-   Anggota 3: Syakila Naira (2408107010034)

