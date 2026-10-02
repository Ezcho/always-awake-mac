Source: https://no-sleep-pika.online/guide/id/keep-mac-awake/
Language: id

MAC GUIDE · 2026-10-02

# Cara menjaga Mac tetap aktif: clamshell, caffeinate, dan pika

Bandingkan daya dan mode clamshell, perintah Terminal, serta pika. Pahami syarat tutup layar, penguncian, batasan, dan cara mengakhiri sesi.

## Pilih sesuai tugas

Layar mati, layar terkunci, dan sistem tidur berbeda. Mac terkunci masih dapat bekerja. Untuk monitor eksternal periksa clamshell; untuk tugas sementara dengan tutup terbuka gunakan caffeinate; untuk pekerjaan tertutup tanpa monitor eksternal pertimbangkan pika dengan layanan pembantunya.

## 1. Daya dan mode clamshell

Saat tutup terbuka, hubungkan daya, monitor yang didukung, keyboard dan mouse. Pastikan semuanya bekerja sebelum menutup. Monitor yang memasok daya mungkin menggantikan pengisi daya sesuai spesifikasi. Pengisi daya saja tidak membentuk konfigurasi ini. Jumlah dan resolusi layar bergantung pada model; setujui aksesori sebelum menutup.

[Apple · External displays](https://support.apple.com/en-us/102501)

## Pengaturan saat tutup terbuka

Pada laptop tersambung daya, cari pengaturan pencegahan tidur otomatis saat layar mati di Pengaturan Sistem → Baterai → Opsi. Nama dan lokasinya berbeda menurut macOS dan model. Tetap aktifkan kata sandi penguncian. Pengaturan ini bukan jaminan mencegah tidur akibat menutup layar. Catat pilihan sebelumnya.

[Apple · Sleep and wake settings](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

## 2. Gunakan caffeinate sementara

Buka Terminal dan jalankan perintah berikut. caffeinate sudah ada di macOS dan tidak memerlukan sudo. Ini mencegah tidur karena tidak ada aktivitas, tetapi layar boleh mati. Biarkan proses berjalan dan tekan Control+C pada Terminal tersebut untuk berhenti. Tidak ada keluaran adalah normal. Permintaan dilepas saat proses selesai.

```
caffeinate -i
```

## Durasi, layar, dan perintah

Contoh pertama berlaku 3.600 detik atau satu jam. Contoh kedua juga menjaga layar selama 1.800 detik atau setengah jam; hapus -d jika tidak perlu. Contoh ketiga benar-benar menjalankan make sampai selesai, jadi gunakan hanya pada proyek yang hendak dibangun. Peluncur yang segera keluar dapat selesai sebelum tugas latar belakang. Jika menjalankan utilitas, -t tidak digunakan.

```
caffeinate -i -t 3600
```

```
caffeinate -di -t 1800
```

```
caffeinate -i make
```

## Bagaimana saat tutup ditutup?

-i berlaku untuk tidur sistem karena tidak aktif, -d untuk layar. Menutup tutup merupakan kondisi berbeda, bukan jaminan operasi tanpa monitor. -s hanya berlaku pada daya AC; -u menyatakan aktivitas pengguna dan dapat menyalakan layar. Pilih opsi sesuai fungsi yang didokumentasikan.

## 3. Instal pika

pika mendukung macOS 13 ke atas, Apple Silicon dan Intel. PKG resmi lengkap memasang aplikasi dan layanan pembantu administrator. Selesaikan autentikasi dan persetujuan macOS sendiri. Buka /Applications/pika.app, periksa layanan, aktifkan Session, pilih Monitor OFF jika perlu, lalu tutup layar. Pencegahan tidur disiapkan sebelumnya; kebijakan layar diterapkan setelah ditutup. Saat terbuka, Monitor hanya menyimpan pilihan. Session OFF memulihkan pengaturan tanpa langsung mematikan layar. Menutup jendela tidak keluar dari aplikasi.

[Unduh pika · 1.0.13](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)

[Bantuan instalasi](https://no-sleep-pika.online/install/)

## Periksa lalu akhiri

Uji tugas singkat, catat waktu, kemudian periksa log dan kemajuannya. Ini prosedur uji yang disarankan, bukan klaim semua model telah diuji. pmset -g assertions hanya membaca permintaan saat ini dan tidak membuktikan koneksi jaringan atau kesinambungan saat ditutup. man caffeinate membuka manual lokal.

```
pmset -g assertions
```

```
man caffeinate
```

## Kunci layar, jaringan, panas

Terkunci tidak selalu berarti tidur. Wi-Fi, VPN, batas API, persetujuan tertunda, atau kesalahan aplikasi dapat menghentikan pekerjaan; pika tidak melanjutkan percakapan AI atau memperbaiki jaringan. Gunakan permukaan keras dan berventilasi, bukan tas. Proteksi baterai, suhu atau gangguan layanan dapat mengakhiri sesi dan tidak menjamin semua panas berlebih atau kehabisan daya dapat dicegah.

## Sumber dan cakupan

Ditulis oleh pembuat no-sleep-pika dan mencakup aplikasi sendiri. Berdasarkan dokumen Apple, manual caffeinate(8) macOS, serta dokumentasi dan implementasi pika 1.0.13. Bukan dukungan resmi Apple atau penyedia AI. Jalankan hanya selama diperlukan.

- [Apple: If your external display is dark or low resolution](https://support.apple.com/en-us/102501)

- [Apple: Set sleep and wake settings for your Mac](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

- [Apple: Allow USB and other accessories](https://support.apple.com/en-us/102282)

- `man caffeinate` · macOS System Manager’s Manual

Ditulis oleh pembuat no-sleep-pika; mencakup aplikasi kami.

[Unduh pika](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)[Panduan MacBook tertutup →](https://no-sleep-pika.online/guide/id/macbook-lid-closed/)[Markdown](https://no-sleep-pika.online/guide/id/keep-mac-awake/index.md)
