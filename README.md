# Lua Motion Converter

Aplikasi desktop untuk mengkonversi file motion Lua dari derajat ke radian secara otomatis.

## Fitur
- Antarmuka grafis modern menggunakan [ttkbootstrap](https://ttkbootstrap.readthedocs.io/)
- Memilih file input dan output dengan dialog
- Konversi otomatis dari derajat ke radian
- Progress bar dan log aktivitas
- Ubah tampilan dengan tema : 
'litera', 'cosmo', 'flatly', 'journal', 'lumen', 'minty', 'pulse', 'sandstone', 'united', 'yeti'
'cyborg', 'darkly', 'solar', 'superhero' (Tema Gelap)



## Cara Install & Jalankan

1. **Clone repo:**
   ```bash
   git clone https://github.com/youngIcom/ConverterDegreeToRadian.git
   cd ConverterDegreeToRadian
   ```

2. **Install dependencies:**
   ```bash
   pip install ttkbootstrap pillow
   ```

3. **Jalankan aplikasi:**
   ```bash
   python main.py
   ```

## Cara Pakai

1. Klik **Pilih File Input** untuk memilih file Lua yang ingin dikonversi.
2. Klik **Simpan Hasil Ke** untuk menentukan lokasi file hasil konversi.
3. Klik **KONVERSI SEKARANG** untuk memulai proses konversi.
4. Status dan log aktivitas akan tampil di bagian bawah aplikasi.

## Struktur Output

File hasil konversi akan berisi data motion Lua dengan sudut dalam satuan radian.

---

**Dibuat oleh Yesaya | youngIcom**