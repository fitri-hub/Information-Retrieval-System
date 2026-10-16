
import os

from indexing import muat_dan_index_dataset, INDEX_DIR
from search_engine import cari_dokumen


def tampilkan_menu(dataset_siap, jumlah_dokumen):
    print("\n" + "=" * 50)
    print("          INFORMATION RETRIEVAL SYSTEM")
    print("=" * 50)

    if dataset_siap:
        status_dataset = "Sudah dimuat"
    else:
        status_dataset = "Belum dimuat"

    if os.path.isdir(INDEX_DIR) and dataset_siap:
        status_index = "Tersedia"
    else:
        status_index = "Belum tersedia"

    print(f"Status Dataset : {status_dataset}")
    print(f"Status Index   : {status_index}")
    print(f"Jumlah Dokumen : {jumlah_dokumen}")
    print("-" * 50)

    print("[1] Load & Index Dataset")
    print("[2] Search Query")
    print("[3] Show Dataset Information")
    print("[4] Show Index Information")
    print("[5] Exit")
    print("=" * 50)


def tampilkan_info_dataset(dokumen):
    if not dokumen:
        print("\nDataset belum dimuat. Pilih menu 1 terlebih dahulu.")
        return

    jumlah_per_sumber = {}

    for item in dokumen:
        sumber = item["sumber"]
        jumlah_per_sumber[sumber] = (
            jumlah_per_sumber.get(sumber, 0) + 1
        )

    print("\n" + "=" * 50)
    print("             DATASET INFORMATION")
    print("=" * 50)

    for sumber, jumlah in sorted(jumlah_per_sumber.items()):
        print(f"{sumber:<20}: {jumlah} dokumen")

    print("-" * 50)
    print(f"Total dokumen       : {len(dokumen)}")
    print("=" * 50)


def tampilkan_info_index(dataset_siap, jumlah_dokumen):
    print("\n" + "=" * 50)
    print("              INDEX INFORMATION")
    print("=" * 50)

    if dataset_siap and os.path.isdir(INDEX_DIR):
        print("Status              : Index tersedia")
        print(f"Jumlah dokumen      : {jumlah_dokumen}")
        print(f"Lokasi index        : {INDEX_DIR}")
    else:
        print("Status              : Index belum tersedia")
        print("Silakan pilih menu 1 terlebih dahulu.")

    print("=" * 50)


def tampilkan_hasil(hasil):
    if not hasil:
        print("\nTidak ada dokumen yang cocok dengan query.")
        return

    print("\n" + "=" * 60)
    print("HASIL PENCARIAN")
    print("=" * 60)

    for nomor, item in enumerate(hasil, start=1):
        print(f"\nPeringkat : {nomor}")
        print(f"Judul     : {item['judul']}")
        print(f"Sumber    : {item['sumber']}")
        print(f"Skor      : {item['skor']:.4f}")
        print(f"Dokumen   : {item['konten_asli'][:500]}")
        print("-" * 60)


def main():
    dokumen = []
    dataset_siap = False

    while True:
        tampilkan_menu(dataset_siap, len(dokumen))
        pilihan = input("Pilih menu (1-5): ").strip()

        if pilihan == "1":
            try:
                print("\nMemuat dataset dan membuat index...")
                dokumen, _ = muat_dan_index_dataset()
                dataset_siap = True

                print("\nIndexing berhasil!")
                print(f"Jumlah dokumen: {len(dokumen)}")

                tampilkan_info_dataset(dokumen)

            except (OSError, ValueError) as error:
                dokumen = []
                dataset_siap = False
                print(f"\nGagal memuat dataset: {error}")

        elif pilihan == "2":
            if not dataset_siap:
                print("\nSilakan Load & Index Dataset terlebih dahulu.")
                continue

            query = input("\nMasukkan query pencarian: ").strip()

            hasil = cari_dokumen(
                query_pengguna=query,
                dokumen=dokumen,
                jumlah_hasil=5
            )

            tampilkan_hasil(hasil)

        elif pilihan == "3":
            tampilkan_info_dataset(dokumen)

        elif pilihan == "4":
            tampilkan_info_index(dataset_siap, len(dokumen))

        elif pilihan == "5":
            print("\nTerima kasih. Program selesai.")
            break

        else:
            print("\nPilihan tidak valid. Masukkan angka 1-5.")


if __name__ == "__main__":
    main()
