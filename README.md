# Rekayasawan Paripurna

Buku Quarto dan deck kuliah Reveal.js dalam bahasa Indonesia. Konsep utama berasal dari Armein Z. R. Langi. Paket ini menyusun percakapan 1 Oktober 2026 menjadi materi belajar, dengan rujukan publik untuk DRM, DSRM, PICOC, dan digital twin.

## Mulai membaca

- `reading/buku.html`: buku lengkap dalam satu HTML, dapat dibuka tanpa internet.
- `reading/kuliah.html`: deck Reveal.js lengkap, dengan catatan pengajar.
- `book/_book/index.html`: buku Quarto dengan navigasi per bab. Buka melalui server lokal agar pencarian berfungsi.

## Render sumber

Install Quarto dari https://quarto.org/docs/get-started/. Dari direktori paket:

~~~bash
quarto render book
quarto render slides
~~~

Untuk membangun ulang seluruh paket, termasuk HTML mandiri, jalankan:

~~~bash
python scripts/build-all.py
~~~

Skrip memakai SVG yang telah disertakan; Node dan Mermaid tidak diperlukan untuk render teks. Pada Windows, gunakan `py` bila perintah Python adalah `py`.

Deck berada di `slides/_slides/kuliah.html`. Tekan panah untuk navigasi, `O` untuk overview, `S` untuk catatan pengajar. Speaker view paling andal melalui server lokal, misalnya `python -m http.server 8000`, kemudian buka `http://localhost:8000/reading/kuliah.html`.

## Isi yang dapat diedit

- `book/chapters/`: 14 bab utama.
- `book/appendices/`: glosarium, lembar kerja, panduan kuliah, jawaban latihan.
- `slides/kuliah.qmd`: seluruh slide beserta catatan pengajar.
- `assets/diagrams/*.mmd`: sumber Mermaid. SVG siap pakai tersedia berdampingan.
- `scripts/simulate_food.py`: contoh simulasi sintetik yang dapat dijalankan.
- `data/`: data hasil simulasi, bukan data lapangan.
- `references.bib`: rujukan terstruktur.

Perubahan teks QMD dan tabel cukup dirender ulang. Setelah mengubah diagram `.mmd`, jalankan `scripts/render-diagrams.mjs` dengan Node, Playwright, dan Mermaid lokal, atau ekspor SVG memakai Mermaid CLI. Diagram SVG tidak memerlukan JavaScript saat dibaca.

Diagram dengan awalan `slides-` memakai susunan khusus layar lebar. Untuk generator yang disertakan, tentukan `TISE_MERMAID_JS` sebagai path berkas `mermaid.min.js`. `TISE_BROWSER_EXE` bersifat opsional untuk memilih executable Chromium. Buku dan deck menggunakan sumber visual terpisah ketika orientasi layar memerlukan susunan berbeda.

## Isi dan penggunaan kuliah

Paket berisi 14 bab, empat lampiran, 64 slide, 78 tabel dalam buku mandiri, dan 32 gambar yang ditampilkan dalam buku. Catatan pengajar tersedia pada 63 slide materi. Enam sesi berdurasi 90 menit, latihan per bab, delapan lembar kerja, dan rubrik tersedia di lampiran. Angka durasi merupakan rancangan pengajaran yang dapat disesuaikan.

## Status pengetahuan

TISE 1.0–3.0 mengikuti dokumen konseptual penulis 23 Agustus 2026. EASTF dengan lapisan ekosistem, tahapan gagasan–model–digital twin–realisasi, dan definisi rekayasawan paripurna merupakan rumusan serta sintesis percakapan ini. Angka contoh, target, kurva kapabilitas, dan simulasi pangan adalah ilustrasi, bukan hasil penelitian empiris. Paket ini tidak menyatakan bahwa TISE telah mencapai tingkat validasi tertentu.
