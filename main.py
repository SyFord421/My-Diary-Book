import sqlite3
from datetime import datetime
import time

class DiaryBook:
    """inisiasi class utama agar lebih rapih"""
    def __init__(self, DB_Name="mydiarybook.db"):
        self.database = DB_Name
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS notes 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp TEXT)''')

    def add_content(self):
        content = input("Ceritakan bagaimana perasaanmu hari ini.\n: ")
        timestamp = datetime.now().strftime("%A, %d-%m-%Y %H:%M")
        if self.validate_input(content):
            self.cursor.execute('''INSERT INTO notes (content, timestamp) VALUES(?, ?)''', (content, timestamp))
            self.conn.commit()
            print("[√] Catatan tersimpan!")

    def show_all(self):
        all_data = self.cursor.execute('SELECT * FROM notes').fetchall()
        if not all_data:
            print("[E] Diary masih kosong nih...")
            return
        print("\n" + "="*30)
        print("      ISI DIARY KAMU      ")
        print("="*30)
        for i in all_data:
            print(f"[{i[0]}] {i[2]}")
            print(f"Content: {i[1]}")
            print("-" * 20)

    def delete_note(self):
        try:
            self.show_all()
            id_target = input("\n[!] Masukan ID yang mau dihapus: ")
            if not id_target.isdigit():
                print("[E] ID harus angka ya, jangan masukin harapan palsu... 🙄")
                return
            self.cursor.execute('''DELETE FROM notes WHERE id = ?''', (id_target,))
            self.conn.commit()
            print(f"[!] ID {id_target} berhasil dibuang, kayak kenangan mantan!")
        except Exception as e:
            print(f"[E] Error pas hapus: {e}")

    def validate_input(self, text):
        if not text.strip():
            print("[!] Error: null Mau simpan apa? kosong banget kayak isi hatiku 🥀")
            return False
        if len(text) < 5:
            print("[E] Masa Curhat Singkat banget.. kayak chat sama mantan aja")
            return False
        return True

    def update_note(self):
        try:
            self.show_all()
            id_target = input("[!] Masukan ID yang mau di-edit\n: ")
            self.cursor.execute('SELECT * FROM notes WHERE id = ?', (id_target,))
            target = self.cursor.fetchone()
            if target:
                new_content = input(f"Catatan lama: '{target[1]}'\nUbah jadi apa?: ")
                if self.validate_input(new_content):
                    self.cursor.execute('UPDATE notes SET content = ? WHERE id = ?', (new_content, id_target))
                    self.conn.commit()
                    print("[√] Kenangan berhasil diperbarui, semoga hati juga ya! ✨")
            else:
                print("[E] ID nggak ketemu, kayak nyari kepastian di hubungan ini..")
        except Exception as e:
            print(f"[E] Error {e}: Solusi? Cari pacar baru atau debug ulang.")

if __name__ == "__main__":
    diary = DiaryBook()
    while True:
        try:
            print("\n 1. Tambah\n", "2. Tampilkan semua\n", "3. Hapus catatan\n", "4. Ubah catatan\n", "5. Keluar")
            while True:
                choose = input("Masukan Pilihan[1/2/3/4/5]: ")
                if choose.isdigit():
                    break
                else:
                    print("[!] Aduh masukin yang bener lah bukan janji manis doang")

            if choose == '1':
                diary.add_content()
            elif choose == '2':
                diary.show_all()
            elif choose == '3':
                diary.delete_note()
            elif choose == '4':
                diary.update_note()
            elif choose == '5':
                break
            else:
                ("Hmmmmm")
        except Exception as e:
            print(f"[E] {e}")
        
