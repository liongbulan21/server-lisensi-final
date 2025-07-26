import sqlite3

# Nama file database yang akan dibuat
DATABASE_FILE = 'licenses.db'

# Membuat koneksi ke database (akan membuat file jika belum ada)
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

# Membuat tabel 'licenses' jika belum ada
# PRIMARY KEY memastikan setiap license_key unik
cursor.execute('''
    CREATE TABLE IF NOT EXISTS licenses (
        license_key TEXT PRIMARY KEY,
        device_id TEXT,
        customer_name TEXT NOT NULL
    )
''')

print(f"Database '{DATABASE_FILE}' dan tabel 'licenses' berhasil disiapkan.")

# Menutup koneksi
conn.commit()
conn.close()