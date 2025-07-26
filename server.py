from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE_FILE = 'licenses.db'

def query_db(query, args=(), one=False):
    """Fungsi helper untuk query database."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    """Fungsi helper untuk mengubah data di database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(query, args)
    conn.commit()
    conn.close()

@app.route('/verify_license', methods=['POST'])
def verify_license():
    data = request.get_json()
    license_key = data.get('license_key')
    device_id = data.get('device_id')

    # Cari lisensi di database
    license_data = query_db('SELECT * FROM licenses WHERE license_key = ?', [license_key], one=True)

    if not license_data:
        return jsonify({'status': 'error', 'message': 'Kunci lisensi tidak ditemukan atau tidak valid.'})

    stored_device_id = license_data['device_id']

    if not stored_device_id:
        # Aktivasi lisensi baru
        execute_db('UPDATE licenses SET device_id = ? WHERE license_key = ?', [device_id, license_key])
        return jsonify({'status': 'success', 'message': 'Lisensi berhasil diaktivasi.'})
    
    elif stored_device_id == device_id:
        return jsonify({'status': 'success', 'message': 'Lisensi valid untuk perangkat ini.'})
        
    else:
        return jsonify({'status': 'error', 'message': 'Lisensi ini telah digunakan di perangkat lain.'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)