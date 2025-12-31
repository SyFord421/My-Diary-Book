import os
import json
from datetime import datetime


class Pen:
    """Class untuk merepresentasikan satu entri catatan diary. Menyimpan isi konten dan stempel waktu otomatis."""
    def __init__(self, content):
        self.content = content
        self.timestamp = datetime.now().strftime("%A, %d-%m-%Y")

    def to_dict(self):
        """Menyatukan catatan, timestamp dan mengubahnya ke dalam bentuk Dictionary Untuk di simpan di file json"""
        return {
        'content' : self.content,
        'timestamp' : self.timestamp
        }

class DiaryBook:
    """Class utama untuk mengelola buku catatan."""
    def __init__(self, FILE_DB="diary_db.json"):
        self.FILE_DB = FILE_DB
        self.create = self.load_json()

    def load_json(self):
        """Membaca data dari file json mengembalikan list kosong"""
        if not os.path.exists(self.FILE_DB):
            return []
        try:
            with open(self.FILE_DB, 'r') as f:
                return json.load(f)
        except  (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_to_json(self):
        """Menyimpan Kedalam File Json"""
        with open (self.FILE_DB, 'w') as f:
            json.dump(self.create, f, indent=2)

    def add_content(self):
        """Menambahkan konten/cacatan"""
        content = input("Ceritakan bagaimana perasaanmu?\n: ")
        if self.validate_input(content):
            new_cont = Pen(content)
            self.create.append(new_cont.to_dict())
            self.save_to_json()
            print("Sipp data Sudah di Simpan")
        else:
            print("Kamu bercanda?")

    def show_all(self):
        """Menunjukan  semua isi yang tersimpan"""
        data = self.load_json()
        if not data:
            print ("\n📭 Buku harian masih kosong...")
            return
        print("\n" + "—"*15 + " MY SECRET DIARY " + "—"*15)
        for index, entry in enumerate(data):
            print(f"[{index}] {entry['timestamp']}")
            print(f"Content: {entry['content']}")
            print("-" * 47)

    def delete_note(self):
        """Menghapus data yang tersimpan"""
        data = self.load_json()
        self.show_all()
        if data:
            try:
                target = int(input("Masukan Nomor catatan yang akan di hapus: "))
                confirm = input("Yakin mau hapus?[y/n]: ")
                if confirm == 'y':
                    removed = data.pop(target)
                    self.create = data
                    self.save_to_json()
                    print(f"✅ Catatan '{removed['content'][:20]}...' berhasil dihapus!")
                if confirm == 'n':
                    return
            except (IndexError, ValueError):
                print("❌ Nomornya salah tuh, coba cek lagi ya!")

    def update_note(self):
        """mengubah isi catatan"""
        data = self.load_json()
        self.show_all()
        if data:
            try:
                target = int(input("\nNomor catatan yang mau diubah: "))
                print(f"Isi lama: {data[target]['content']}")
                new_text = input("Tulis isi baru (kosongkan untuk membatalkan):  ")
                if new_text:
                    data[target] ['content'] = new_text
                    data[target] ['timestamp'] += " (Edited)"
                    self.create = data
                    self.save_to_json()
                    print("✅ Catatan berhasil diperbarui!")
            except (IndexError, ValueError):
                print("❌ Input tidak valid")

    def search_by_date(self, date_query):
        """Mencari Catatan yang tersimpan Berdasarkan tanggal dan hari"""
        results = [entry for entry in self.create if date_query in entry ['timestamp']]
        if not results:
            print (f"📭 Tidak ada catatan di tanggal {date_query}")
            return
        print (f"\n📬 Hasil Pencarian tanggal: {date_query}")
        for index, entry in enumerate(results):
            print (f"[{index}] {entry['timestamp']}")
            print (f"Content:\n\n  {entry['content']}")
            print("—"*30)

    def validate_input(self, text):
        """Fungsi memvalidasi Input yang masuk"""
        if not text.strip():
            print("❌ Lu mau simpan apa? Angin?")
            return False
        if len(text) < 5:
            print("❌  Yakin cuma 5 karakter?")
            return False
        return True



if __name__ == "__main__":
    """Menu Utama"""
    db = DiaryBook()
    while True:
        print("\n" + "▥"*10 + " My DIARY Book " + "▥" *10)
        print("1. 📝 Tulis Cerita Baru")
        print("2. 📖 Baca Semua Catatan")
        print("3. 🔍 Cari Berdasarkan Tanggal")
        print("4. ✏️  Ubah Catatan")
        print("5. 🗑️  Hapus Kenangan (Delete)")
        print("6. 🚪 Keluar")
        print("—" * 36)
        
        pilihan = input("Mau lakuin apa hari ini? (1-6): ")
        
        if pilihan == '1':
            db.add_content()
        elif pilihan == '2':
            db.show_all()
        elif pilihan == '3':
            tgl = input("Masukan tanggal (Contoh: Wednesday): ")
            db.search_by_date(tgl)
        elif pilihan == '4':
            db.update_note()
        elif pilihan == '5':
            db.delete_note()
        elif pilihan == '6':
            print("\nGoodBye. Sampai Jumpa lagi lain waktu")
            break
        else:
            print("\n❌ Pilihannya cuma 1-6 ya, manis. Coba lagi!")
