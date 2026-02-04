import sqlite3
from datetime import datetime

class DiaryBook:
    """Class utama untuk mengelola buku catatan yang lebih rapi."""
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
        content = input("Ceritakan bagaimana perasaanmu hari ini, sayang?\n: ")
        timestamp = datetime.now().strftime("%A, %d-%m-%Y %H:%M")
        if self.validate_input(content):
            self.cursor.execute('''INSERT INTO notes (content, timestamp) VALUES(?, ?)''', (content, timestamp))
            self.conn.commit()
            print("[!] Catatan tersimpan!")

    def show_all(self):
        all_data = self.cursor.execute('SELECT * FROM notes').fetchall()
        if not all_data:
            print("[!] Diary masih kosong nih...")
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
                print("[!] ID harus angka ya, jangan masukin harapan palsu... 🙄")
                return
            self.cursor.execute('''DELETE FROM notes WHERE id = ?''', (id_target,))
            self.conn.commit()
            print(f"[!] ID {id_target} berhasil dibuang, kayak kenangan mantan!")
        except Exception as e:
            print(f"[!] Error pas hapus: {e}")

    def validate_input(self, text):
        if not text.strip():
            print("[!] Mau simpan apa?")
            return False
        if len(text) < 5:
            print("[!] Terlalu singkat")
            return False
        return True

if __name__ == "__main__":
    diary = DiaryBook()
    diary.show_all()
