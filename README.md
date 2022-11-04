# Schedule planner for control laboratory with PyQT5 using “gspread” API
Proyek pembuatan GUI dengan python melalui interface PyQT5 dalam rangka pencaslaban kendali 2022

Required Module
  - PyQT5
  - Numpy
  - Gspread

Terdapat 3 buah laman navigasi pada program yaitu Landing Page, Laman Praktikan, dan Laman Aslab.
## Tata Cara Penggunaan 
  1. Run Program Landing_Page.py untuk membuka laman landing Page
  2. Jika ingin masuk sebagai praktikan, tekan tombol praktikan. 
  3. Jika ingin masuk sebagai Aslab, masukan password "password123" lalu tekan tombol login
  4. Silahkan gunakan program sesuai dengan identitas yang digunakan untuk login
  5. Tekan tombol clear apabila ingin menghapus tabel jadwal praktikum
  
  **Sebagai Praktikan**
  
  1. Tunggu sampai counter berada di urutan kelompok anda
  2. Pilih jadwal praktikum yang terdiri dari hari/tanggal, modul, dan sesi sesuai dengan yang anda inginkan
  3. Tekan tombol "Simpan Jadwal"
  4. Apabila jadwal bentrok, akan ada indikator keterangan pilihan anda
  
  **Sebagai Aslab**
  
  1. Pilih Sesi praktikum yang anda inginkan
  2. Pilih tanggal praktikum yang anda inginkan
  3. Pilih Modul yang anda inginkan
  4. Tekan tombol "Save"
  5. Silahkan cek kembali pilihan yang anda inginkan
 
 ## Fitur yang terdapat pada program antara lain
 
  **Sebagai Aslab**
  
    - Input Sesi Aslab (Tanggal, Waktu Sesi, Kode Aslab)
    - Error Handling apabila sesi telah digunakan
    - Terkoneksi dengan google sheet pengambilan jadwal
  
  
  **Sebagai Praktikan**
  
    - Input Sesi Praktikan (Tanggal, Waktu Sesi, Kode Aslab)
    - Counter urutan praktikan untuk mengambil jadwal
    - Terkoneksi dengan google sheet pengambilan jadwal
    - Error handling apabila sesi telah diisi
    
  
