#ZMATH

**ZMATH: Galactic Target** adalah sebuah game edukasi berbasis tipe mengetik cepat (*speed typing*) dan berhitung matematika yang dibangun menggunakan *library* **Pygame**. Pemain berperan sebagai pilot kapal induk yang harus menghancurkan alien yang datang dengan cara menyelesaikan operasi matematika secepat mungkin.

---

## 🛠️ Prasyarat Sistem & Instalasi

Game ini memerlukan **Python versi 3.12** untuk memastikan kompatibilitas penuh dengan seluruh modul yang digunakan.

### 1. Instalasi Python 3.12

Pastikan Anda sudah menginstal Python 3.12 di perangkat Anda. Jika belum, silakan unduh melalui website resmi [python.org](https://www.python.org/downloads/).

> **Catatan:** Jangan lupa mencentang pilihan **"Add Python to PATH"** saat proses instalasi di Windows.

### 2. Kloning Repository (Optional)

Unduh atau klon projek ini dari GitHub ke komputer lokal Anda:

```bash
git clone https://github.com/ALmruff/Zmath.git
cd Zmath

```

### 3. Instalasi Dependency via Terminal

Game ini membutuhkan pustaka pihak ketiga, yaitu **Pygame**. Buka Terminal (macOS/Linux) atau Command Prompt/PowerShell (Windows) di folder projek ini, lalu jalankan perintah berikut:

```bash
pip install pygame

```

---

## 🚀 Cara Menjalankan Game

Setelah seluruh proses instalasi selesai, Anda dapat langsung menjalankan game dengan mengetik perintah berikut di terminal:

```bash
python main.py

```

*(Ganti `main.py` dengan nama file Python game kamu jika namanya berbeda).*

---

## 🎮 Panduan Kontrol Tombol

Untuk menghindari konflik *input* saat bermain, game ini memisahkan tombol navigasi menu dan tombol aksi mengetik secara penuh:

### **Di Dalam Menu Utama (Input Nama)**

* **`A` - `Z` / `0` - `9`**: Mengetik nama pilot (maksimal 10 karakter).
* **`BACKSPACE`**: Menghapus karakter nama jika ada salah ketik.
* **`ENTER`**: Mengonfirmasi nama pilot dan meluncurkan misi (memulai game).

### **Di Dalam Gameplay (Pertempuran)**

* **`ESC` (Escape)**: Menjeda permainan (*Pause Game*) untuk membuka **Command Interface**.
* **`A` - `Z`**: Membidik alien target. Tekan tombol huruf yang sesuai dengan kode awalan di dalam tanda kurung siku `[...]` pada alien yang ingin ditembak.
* **`0` - `9`** dan **`-` (Minus)**: Mengetik jawaban matematika setelah alien berhasil dibidik.
* **`BACKSPACE`**: Mengosongkan kolom input jawaban jika Anda salah menghitung.

### **Di Dalam Menu Pause (Command Interface)**

* **`W` / `S`** atau **`Panah Atas` / `Panah Bawah`**: Navigasi memilih menu (`RESUME MISSION` atau `ABORT MISSION`).
* **`ENTER`**: Mengonfirmasi pilihan menu yang disorot.
* **`ESC` (Escape)**: Menutup menu pause dan langsung melanjutkan pertempuran secara instan.

### **Di Halaman Akhir (Game Over)**

* **`R`**: Memulai ulang permainan dari Level 1 (*Restart Mission*).
* **`ESC` (Escape)**: Keluar dari aplikasi game (*Quit to Desktop*).

---

## 🕹️ Mekanisme & Cara Bermain

1. **Pendaftaran Pilot**: Di awal game, masukkan nama pilot Anda untuk mencatat skor ke dalam sistem *Global Leaderboard*.
2. **Sistem Penargetan (Targeting System)**: Alien akan turun dari atas secara acak. Pilih satu alien dengan menekan huruf awalan kode mereka. Garis putus-putus hijau akan muncul dari turret kapal induk menuju alien yang sedang Anda bidik.
3. **Eksekusi Jawaban**: Selesaikan soal matematika (Penjumlahan, Pengurangan, Perkalian, atau Pembagian tergantung level) yang tertera pada alien tersebut, lalu ketik jawabannya. Jika benar, alien akan meledak dalam efek partikel dan Anda mendapatkan poin skor.
4. **Kenaikan Level**: Setiap berhasil menjawab 15 soal, game akan naik level (Maksimal Level 25). Semakin tinggi level, variasi soal matematika akan semakin menantang dan pergerakan alien akan semakin cepat.
5. **Kondisi Kalah (Game Over)**: Jika ada salah satu alien yang berhasil lolos dan menyentuh deck kapal induk di bagian bawah layar, pertahanan pangkalan akan hancur dan game berakhir. Skor tertinggi Anda akan otomatis disimpan dalam file local database `leaderboard_v2.json`.
