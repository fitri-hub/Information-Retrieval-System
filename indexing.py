
import os
import shutil
import pandas as pd

from whoosh.index import create_in
from whoosh.fields import Schema, ID, TEXT

from preprocessing import preprocessing


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
INDEX_DIR = os.path.join(BASE_DIR, "storage", "index")

SCHEMA = Schema(
    doc_id=ID(stored=True, unique=True),
    judul=TEXT(stored=True),
    sumber=ID(stored=True),
    konten=TEXT(stored=True)
)

SUPPORTED_EXTENSIONS = {".txt", ".md", ".csv"}


def baca_file_teks(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


def muat_dataset():
    dokumen = []
    nomor_dokumen = 1

    if not os.path.isdir(DATASET_DIR):
        raise FileNotFoundError(
            f"Folder dataset tidak ditemukan: {DATASET_DIR}"
        )

    for root, _, files in os.walk(DATASET_DIR):
        for nama_file in sorted(files):
            ekstensi = os.path.splitext(nama_file)[1].lower()

            if ekstensi not in SUPPORTED_EXTENSIONS:
                continue

            path_file = os.path.join(root, nama_file)
            folder_rel = os.path.relpath(root, DATASET_DIR)
            sumber = folder_rel.split(os.sep)[0]

            if ekstensi in {".txt", ".md"}:
                isi = baca_file_teks(path_file)

                if isi.strip():
                    dokumen.append({
                        "doc_id": str(nomor_dokumen),
                        "judul": os.path.splitext(nama_file)[0],
                        "sumber": sumber,
                        "konten_asli": isi,
                        "konten": preprocessing(isi)
                    })
                    nomor_dokumen += 1

            elif ekstensi == ".csv":
                try:
                    tabel = pd.read_csv(
                        path_file,
                        dtype=str,
                        keep_default_na=False,
                        encoding="utf-8"
                    )
                except UnicodeDecodeError:
                    tabel = pd.read_csv(
                        path_file,
                        dtype=str,
                        keep_default_na=False,
                        encoding="latin-1"
                    )

                for nomor_baris, baris in tabel.iterrows():
                    bagian = []

                    for kolom, nilai in baris.items():
                        nilai = str(nilai).strip()

                        if nilai:
                            bagian.append(f"{kolom}: {nilai}")

                    isi = " ".join(bagian)

                    if isi.strip():
                        dokumen.append({
                            "doc_id": str(nomor_dokumen),
                            "judul": (
                                f"{os.path.splitext(nama_file)[0]} "
                                f"- baris {nomor_baris + 1}"
                            ),
                            "sumber": sumber,
                            "konten_asli": isi,
                            "konten": preprocessing(isi)
                        })
                        nomor_dokumen += 1

    return dokumen


def buat_index(dokumen):
    """Membuat ulang index Whoosh berdasarkan dataset terbaru."""
    os.makedirs(os.path.dirname(INDEX_DIR), exist_ok=True)

    if os.path.isdir(INDEX_DIR):
        shutil.rmtree(INDEX_DIR)

    os.makedirs(INDEX_DIR)

    ix = create_in(INDEX_DIR, SCHEMA)
    writer = ix.writer()

    try:
        for item in dokumen:
            writer.add_document(
                doc_id=item["doc_id"],
                judul=item["judul"],
                sumber=item["sumber"],
                konten=item["konten"]
            )

        writer.commit()

    except Exception:
        writer.cancel()
        raise

    return ix


def muat_dan_index_dataset():
    """Memuat dataset lalu membangun index."""
    dokumen = muat_dataset()

    if not dokumen:
        raise ValueError(
            "Tidak ada dokumen yang ditemukan. "
            "Periksa isi folder dataset dan format file."
        )

    ix = buat_index(dokumen)
    return dokumen, ix
