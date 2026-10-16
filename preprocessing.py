
import re

STOPWORDS_ID = {
    "yang", "dan", "di", "ke", "dari", "ini", "itu", "untuk",
    "dengan", "pada", "adalah", "dalam", "tidak", "akan", "juga",
    "ada", "karena", "atau", "sebagai", "oleh", "dapat", "bisa",
    "sudah", "telah", "belum", "lebih", "sangat", "agar", "ia",
    "dia", "mereka", "kami", "kita", "saya", "aku", "kamu",
    "nya", "tersebut", "yaitu", "yakni", "serta", "hingga",
    "saat", "ketika", "antara", "bagi", "para", "sebuah",
    "suatu", "pun", "hanya", "masih", "lagi", "bukan",
    "melalui", "terhadap", "secara", "jadi"
}

# Kamus sederhana untuk mengubah kata ke bentuk dasarnya.
KAMUS_LEMMA = {
    "makanan": "makan",
    "memakan": "makan",
    "dimakan": "makan",
    "termakan": "makan",
    "berjalan": "jalan",
    "berlari": "lari",
    "bermain": "main",
    "permainan": "main",
    "memainkan": "main",
    "menuliskan": "tulis",
    "menulis": "tulis",
    "ditulis": "tulis",
    "penulisan": "tulis",
    "membaca": "baca",
    "dibaca": "baca",
    "bacaan": "baca",
    "pelajar": "ajar",
    "belajar": "ajar",
    "mempelajari": "ajar",
    "pengajaran": "ajar",
    "pendidikan": "didik",
    "mendidik": "didik",
    "berpendidikan": "didik",
    "terbarukan": "baru",
    "pembaruan": "baru",
    "perubahan": "ubah",
    "mengubah": "ubah",
    "diubah": "ubah",
    "penggunaan": "guna",
    "menggunakan": "guna",
    "digunakan": "guna",
    "penelitian": "teliti",
    "meneliti": "teliti",
    "diteliti": "teliti"
}


def case_folding(teks):
    """Mengubah seluruh teks menjadi huruf kecil."""
    return teks.lower()


def tokenisasi(teks):
    """Memisahkan teks menjadi token berupa huruf atau angka."""
    return re.findall(r"\b[a-zA-Z0-9]+\b", teks)


def hapus_stopword(token):
    """Menghapus kata umum yang tidak diperlukan."""
    return [
        kata for kata in token
        if kata not in STOPWORDS_ID
    ]


def lemmatization(token):
    """Mengubah kata yang dikenal menjadi bentuk dasar."""
    return [
        KAMUS_LEMMA.get(kata, kata)
        for kata in token
    ]


def preprocessing(teks):
    """Menjalankan seluruh tahapan preprocessing."""
    teks = case_folding(teks)
    token = tokenisasi(teks)
    token = hapus_stopword(token)
    token = lemmatization(token)

    return " ".join(token)


if __name__ == "__main__":
    teks_contoh = (
        "Para mahasiswa sedang melakukan penelitian "
        "dan menggunakan data untuk pembelajaran."
    )

    print("Teks awal:")
    print(teks_contoh)

    teks_lower = case_folding(teks_contoh)
    print("\nSetelah case folding:")
    print(teks_lower)

    token = tokenisasi(teks_lower)
    print("\nSetelah tokenisasi:")
    print(token)

    token = hapus_stopword(token)
    print("\nSetelah stopword removal:")
    print(token)

    token = lemmatization(token)
    print("\nSetelah lemmatization:")
    print(token)

    print("\nHasil akhir preprocessing:")
    print(" ".join(token))
