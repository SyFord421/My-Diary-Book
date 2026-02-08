import sqlite3
from datetime import datetime
import time
import atexit 
from colorama import Fore, Style, init
import sys

init(autoreset=True)#inisiasi colorama

class DiaryBook:
    """inisiasi class utama agar lebih rapih"""
    def __init__(self, DB_NAME="mydiarybook.db"):
        self.database = DB_NAME
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()
        self.init_db()
        atexit.register(self.cleanup)#untuk membersihkan dan menutup semua koneksi ke database

    def init_db(self):
        """Memastikan Table sudah di buat sebelum memulai"""
        with self.conn:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS notes 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp TEXT)''')

    def cleanup(self):
        """Ini Fungsi Menutup semua koneksi dan Membersihkan pascaprogram"""
        try:
            self.cursor.close()
            print("Perbersihan Berhasil Di Lakukan Sampai Jumpa Di Radio Nasib Selanjutnya...")
        except:
            pass
        
    def search_by_id(self, id_target):
        """Mencari data dengan id"""
        self.cursor.execute('SELECT * FROM notes WHERE id=?', (id_target,))
        result = self.cursor.fetchone()
        if not result:
            return None
        return result

    def search_by_keyword(self, keyword):
        """fungsi mencari dengan kata kunci"""
        keyword = input("[?] Mau cari kata apa di kenanganmu? : ")
        self.cursor.execute("SELECT * FROM notes WHERE content LIKE ?", (f'%{keyword}%',))
        result = self.cursor.fetchall()
        if not result:
            print(f"[!] Nggak ada catatan tentang '{keyword}'. Mungkin kamu udah lupa? 🍃")
        else:
            print(f"Ketemu Ini semua yang berkaitan dengan kata kuncimu{len(result)}")
            for r in result:
                print(f"ID:{r[0]:<5} Memo: {r[1][:30]:<30} TIME: {r[2]:<5}") 
                #untuk menampilkan hasil pencarian [:30] untuk membatasi cuplikan di 30 karakter :<30 untuk memberikan tabel visual agar lebih rapih 
   
    def validate_input(self, text):
        """fungsi untuk memvalidasi input agar tidak kosong atau terlalu pendek"""
        if not text.strip():
            print("[!] Error: null Mau simpan apa? kosong banget kayak isi hatiku 🥀")
            return False
        if len(text) < 5:
            print("[E] Masa Curhat Singkat banget.. kayak chat sama mantan aja")
            return False
        return True

    def add_content(self):
        """untuk menambahkan konten"""
        content = input("Ceritakan bagaimana perasaanmu hari ini.\n: ")
        timestamp = datetime.now().strftime("%A, %d-%m-%Y %H:%M")
        if self.validate_input(content):
            self.cursor.execute('''INSERT INTO notes (content, timestamp) VALUES(?, ?)''', (content, timestamp))
            self.conn.commit()
            print("[√] Catatan tersimpan!")

    def show_all(self):
        """untuk memperlihatkan seluruh data yang tersimpan"""
        query = ('SELECT * FROM notes')
        all_data = self.cursor.execute(query).fetchall()
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
        """untuk satu mengahapus catatan tertentu""" 
        self.show_all()
        id_target = input("\n[!] Masukan ID yang mau dihapus: ")
        self.cursor.execute('SELECT content FROM notes WHERE id = ?', (id_target,))
        note = self.cursor.fetchone()
        if note:
            print(f"Yakin mau hapus: '{note[0]}'?")
            confirm = input("Ketik 'Y' untuk hapus: ").upper()
            if confirm == 'Y':
                self.cursor.execute('DELETE FROM notes WHERE id = ?', (id_target,))
                self.conn.commit()
                print("[!] Kenangan telah dilarungkan ke laut penyesalan...")
            else:
                print("[!] Penghapusan dibatalkan. Masih sayang ya?")
        else:
            print("[E] ID nggak ketemu, kamu mau hapus bayangan?")

    def update_note(self):
        """untuk mengububah catatan"""
        try:
            self.show_all()
            id_target = input("[?] Masukan ID yang mau di-edit\n: ")
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

    def clear_all_db(self):
        """untuk menghapus seluruh catatanyang tersimpan di database"""
        print("[!] PERINGATAN TINDAKAN INI AKAN MENGHAPUS SELURUH DATABASE")
        time.sleep(1)
        print("[!] Kamu yakin mau hapus SEMUA data? Tindakan ini tidak bisa ditarik balik.")
        time.sleep(1)
        print("[*] Kayak waktu kamu bilang 'Kita putus', nggak bisa ditarik lagi lho..")
        confirm = input("Apakah Yakin? Ketik 'SAYONARA' untuk menghapus\n: ").lower().strip()
        if confirm == 'sayonara':
            try:
                self.conn.execute("DELETE FROM notes")
                self.conn.commit()
                print("\n[✔] DATABASE BERHASIL DIKOSONGKAN!")
                print(f"\n[✔] Sayonara to itta Kimi no kimochi wa karanai kedo... 🌸")
                print("Semua perasaan (dan data) yang terbengkalai sudah dibuang.")
                print("Database sekarang sepi, sesepi playlist lagu galau jam 2 pagi.")
            except Exception as e:
                print(f"[E] Tidak ada satupun yang di hapus karena kamu tidak punya apa-apa")
        else:
            print("Chotto Matte!")
            print("Emang bener, ngelepasin itu nggak semudah ngetik kode.. ☕")
            print("[!] Sepertinya kamu lebih menyimpan kesakitan daripada membuang-nya 🥀")
            return

    def main_menu(self):
        while True:
            try:
                print("\n 1. Tambah\n", "2. Tampilkan semua\n", "3. Hapus catatan\n", "4. Ubah catatan\n","5. Hapus semua Kenangan pahit \n", "6. Kembali\n", "7. Keluar")
                while True:
                    choose = input("Masukan Pilihan[1-6]: ").strip()
                    if not choose.isdigit():
                        print("[!] Masukin angka, jangan masukin harapan palsu!")
                        continue 

                    if choose =='1':
                        self.add_content()
                    elif choose =='2':
                        self.show_all()
                    elif choose =='3':
                        self.delete_note()
                    elif choose =='4':
                        self.update_note()
                    elif choose =='5':
                        self.clear_all_db()
                    elif choose =='6':
                        return #untuk fitur kembali
                    if choose == '7':
                        sys.exit()#untuk fitur keluar langsung
                    else:
                        print("masukan angka yang benar")
            except Exception as e:
                print(f"[E] {e}")

if __name__ == "__main__":
    diary= DiaryBook()
    diary.main_menu()