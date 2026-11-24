"""Aplikasi inventaris sederhana berbasis object-oriented programming."""


class Produk:
    """Mewakili satu produk yang disimpan dalam inventaris."""

    def __init__(self, kode: str, nama: str, harga: int, stok: int) -> None:
        self.kode = kode
        self.nama = nama
        self.harga = harga
        self.stok = stok

    @property
    def kode(self) -> str:
        return self.__kode

    @kode.setter
    def kode(self, nilai: str) -> None:
        if not isinstance(nilai, str) or not nilai.strip():
            raise ValueError("Kode produk tidak boleh kosong.")
        self.__kode = nilai.strip().upper()

    @property
    def nama(self) -> str:
        return self.__nama

    @nama.setter
    def nama(self, nilai: str) -> None:
        if not isinstance(nilai, str) or not nilai.strip():
            raise ValueError("Nama produk tidak boleh kosong.")
        self.__nama = nilai.strip()

    @property
    def harga(self) -> int:
        return self.__harga

    @harga.setter
    def harga(self, nilai: int) -> None:
        if isinstance(nilai, bool) or not isinstance(nilai, int) or nilai < 0:
            raise ValueError("Harga harus berupa bilangan bulat yang tidak negatif.")
        self.__harga = nilai

    @property
    def stok(self) -> int:
        return self.__stok

    @stok.setter
    def stok(self, nilai: int) -> None:
        if isinstance(nilai, bool) or not isinstance(nilai, int) or nilai < 0:
            raise ValueError("Stok harus berupa bilangan bulat yang tidak negatif.")
        self.__stok = nilai

    def tambah_stok(self, jumlah: int) -> None:
        self._validasi_jumlah(jumlah)
        self.stok += jumlah

    def kurangi_stok(self, jumlah: int) -> None:
        self._validasi_jumlah(jumlah)
        if jumlah > self.stok:
            raise ValueError("Stok tidak mencukupi.")
        self.stok -= jumlah

    @staticmethod
    def _validasi_jumlah(jumlah: int) -> None:
        if isinstance(jumlah, bool) or not isinstance(jumlah, int) or jumlah <= 0:
            raise ValueError("Jumlah harus berupa bilangan bulat lebih dari nol.")

    @staticmethod
    def format_rupiah(nilai: int) -> str:
        """Mengubah bilangan rupiah menjadi teks dengan pemisah ribuan Indonesia."""
        return f"Rp{nilai:,}".replace(",", ".")


class Inventaris:
    """Mengelola kumpulan produk berdasarkan kode produk."""

    def __init__(self, nama_toko: str) -> None:
        if not isinstance(nama_toko, str) or not nama_toko.strip():
            raise ValueError("Nama toko tidak boleh kosong.")
        self.nama_toko = nama_toko.strip()
        self.__produk: dict[str, Produk] = {}

    @property
    def produk(self) -> tuple[Produk, ...]:
        return tuple(self.__produk.values())

    @classmethod
    def dengan_data_awal(cls, nama_toko: str = "Toko Sederhana") -> "Inventaris":
        inventaris = cls(nama_toko)
        inventaris.tambah_produk(Produk("P001", "Buku Tulis", 5000, 20))
        inventaris.tambah_produk(Produk("P002", "Pulpen", 3000, 35))
        return inventaris

    def tambah_produk(self, produk: Produk) -> None:
        if not isinstance(produk, Produk):
            raise TypeError("Data yang ditambahkan harus berupa objek Produk.")
        if produk.kode in self.__produk:
            raise ValueError(f"Kode produk {produk.kode} sudah terdaftar.")
        self.__produk[produk.kode] = produk

    def cari_produk(self, kode: str) -> Produk:
        if not isinstance(kode, str):
            raise ValueError("Kode produk harus berupa teks.")
        kode_normal = kode.strip().upper()
        try:
            return self.__produk[kode_normal]
        except KeyError:
            raise KeyError(f"Produk dengan kode {kode_normal} tidak ditemukan.") from None

    def total_nilai_stok(self) -> int:
        return sum(produk.harga * produk.stok for produk in self.__produk.values())


def tampilkan_produk(inventaris: Inventaris) -> None:
    if not inventaris.produk:
        print("\nBelum ada produk di inventaris.")
        return

    print(f"\nDaftar produk - {inventaris.nama_toko}")
    print("-" * 68)
    print(f"{'Kode':<10} {'Nama':<24} {'Harga':>14} {'Stok':>8}")
    print("-" * 68)
    for produk in inventaris.produk:
        harga = Produk.format_rupiah(produk.harga)
        print(f"{produk.kode:<10} {produk.nama:<24} {harga:>14} {produk.stok:>8}")


def main() -> None:
    inventaris = Inventaris.dengan_data_awal()
    menu = (
        "\n=== SISTEM INVENTARIS ===\n"
        "1. Lihat semua produk\n"
        "2. Tambah produk\n"
        "3. Tambah stok\n"
        "4. Kurangi stok\n"
        "5. Lihat nilai seluruh stok\n"
        "0. Keluar\n"
    )

    while True:
        print(menu)
        pilihan = input("Pilih menu: ").strip()

        try:
            if pilihan == "1":
                tampilkan_produk(inventaris)
            elif pilihan == "2":
                kode = input("Kode produk: ")
                nama = input("Nama produk: ")
                harga = int(input("Harga (rupiah): "))
                stok = int(input("Stok awal: "))
                inventaris.tambah_produk(Produk(kode, nama, harga, stok))
                print("Produk berhasil ditambahkan.")
            elif pilihan in ("3", "4"):
                produk = inventaris.cari_produk(input("Kode produk: "))
                jumlah = int(input("Jumlah: "))
                if pilihan == "3":
                    produk.tambah_stok(jumlah)
                    print("Stok berhasil ditambahkan.")
                else:
                    produk.kurangi_stok(jumlah)
                    print("Stok berhasil dikurangi.")
            elif pilihan == "5":
                nilai = Produk.format_rupiah(inventaris.total_nilai_stok())
                print(f"Total nilai stok: {nilai}")
            elif pilihan == "0":
                print("Terima kasih. Program selesai.")
                break
            else:
                print("Pilihan tidak tersedia. Silakan pilih menu 0-5.")
        except (ValueError, KeyError) as error:
            print(f"Operasi gagal: {error}")


if __name__ == "__main__":
    main()
