# Multi-Agent Food Ordering System

Tugas ini merupakan implementasi sistem pemesanan makanan berbasis **multi-agent** menggunakan [SPADE](https://spade-mas.readthedocs.io/en/latest/). Sistem ini mensimulasikan interaksi antara agen pelanggan (customer) dan agen penyedia layanan (provider) melalui protokol komunikasi berbasis XMPP.

## Fitur
- Provider memiliki inventori makanan dengan stok terbatas.
- Customer dapat melakukan pemesanan satu atau lebih item.
- Provider merespons permintaan dengan proposal:
  - Jika stok tersedia, mengirim estimasi waktu dan biaya pengiriman.
  - Jika stok habis, menawarkan substitusi menu.
- Customer dapat menerima proposal atau otomatis menerima substitusi.
- Semua interaksi tercatat dalam log CSV dan JSON.

## Struktur Proyek

```
.
├── customer_agent.py      # Definisi agen customer
├── provider_agent.py      # Definisi agen provider
├── logger.py              # Modul pencatat interaksi (CSV & JSON)
├── main.py                # Skenario eksekusi utama
├── conversation_log.csv   # Hasil log CSV
├── conversation_log.json  # Hasil log JSON
└── README.md              # Dokumentasi proyek
```




## Library
- `spade`
- `asyncio`


## Instal dependensi:
'''
pip install spade
'''

## Konfigurasi Akun XMPP

Tugas ini membutuhkan akun XMPP untuk agen.
Contoh:
Provider: providerbaru@xmpp.jp
Customer: customerbaru@xmpp.jp

## Menjalankan Skenario
python main.py

Skenario default:
Provider dijalankan dengan stok terbatas.
Customer memesan beberapa item (Pizza, Burger, Pasta).
Provider menanggapi setiap order sesuai stok.
Logging
Semua percakapan antar agen dicatat dalam:
conversation_log.csv (format tabel)
conversation_log.json (format terstruktur JSON)

