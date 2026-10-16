
import os

from whoosh.index import open_dir
from whoosh.qparser import QueryParser

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from indexing import INDEX_DIR
from preprocessing import preprocessing


def cari_dokumen(query_pengguna, dokumen, jumlah_hasil=5):
    """Mencari dokumen dengan Whoosh dan merankingnya dengan cosine similarity."""

    if not query_pengguna.strip():
        print("Query tidak boleh kosong.")
        return []

    if not dokumen:
        print("Dataset belum dimuat.")
        return []

    query_bersih = preprocessing(query_pengguna)

    if not query_bersih:
        print("Query tidak memiliki kata yang dapat dicari.")
        return []

    if not os.path.isdir(INDEX_DIR):
        print("Index belum dibuat. Pilih menu Load & Index Dataset dahulu.")
        return []

    # Membentuk representasi BoW dari dokumen dan query.
    teks_dokumen = [item["konten"] for item in dokumen]
    vectorizer = CountVectorizer(
        token_pattern=r"(?u)\b\w+\b"
    )

    try:
        matriks_dokumen = vectorizer.fit_transform(teks_dokumen)
        vektor_query = vectorizer.transform([query_bersih])
    except ValueError:
        print("Dokumen belum memiliki kosakata yang dapat diproses.")
        return []

    # Menghitung cosine similarity antara query dan semua dokumen.
    skor_semua = cosine_similarity(
        vektor_query,
        matriks_dokumen
    ).flatten()

    skor_berdasarkan_id = {
        item["doc_id"]: float(skor_semua[i])
        for i, item in enumerate(dokumen)
    }

    # Menggunakan Whoosh untuk mendapatkan dokumen yang cocok.
    ix = open_dir(INDEX_DIR)

    with ix.searcher() as searcher:
        parser = QueryParser("konten", schema=ix.schema)
        query_whoosh = parser.parse(query_bersih)
        hasil_whoosh = searcher.search(query_whoosh, limit=None)

        id_ditemukan = {
            hit["doc_id"] for hit in hasil_whoosh
        }

    # Mengambil skor cosine untuk dokumen hasil pencarian Whoosh.
    hasil = []

    for item in dokumen:
        if item["doc_id"] in id_ditemukan:
            hasil.append({
                "doc_id": item["doc_id"],
                "judul": item["judul"],
                "sumber": item["sumber"],
                "konten_asli": item["konten_asli"],
                "skor": skor_berdasarkan_id[item["doc_id"]]
            })

    # Mengurutkan dari skor cosine tertinggi ke terendah.
    hasil.sort(key=lambda item: item["skor"], reverse=True)

    return hasil[:jumlah_hasil]
