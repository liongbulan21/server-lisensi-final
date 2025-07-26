from flask import Flask, request, render_template, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'kunci-rahasia-yang-super-aman'
DATABASE_FILE = 'licenses.db'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = '@wowo*#123' # Ganti dengan password kuat

# Fungsi helper dari server API bisa disalin atau diimpor
def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(query, args)
    conn.commit()
    conn.close()

# Rute Autentikasi (Tidak berubah)
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # ... (logika login tidak berubah)
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USERNAME and request.form['password'] == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau Password salah.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Rute Panel Admin (Dimodifikasi untuk SQLite)
@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    licenses = query_db('SELECT * FROM licenses ORDER BY customer_name')
    return render_template('dashboard.html', licenses=licenses)

@app.route('/add', methods=['POST'])
def add_license():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    license_key = request.form['license_key']
    customer_name = request.form['customer_name']
    
    try:
        # device_id awalnya kosong (NULL)
        execute_db('INSERT INTO licenses (license_key, customer_name, device_id) VALUES (?, ?, ?)',
                   [license_key, customer_name, None])
        flash('Lisensi berhasil ditambahkan.', 'success')
    except sqlite3.IntegrityError:
        flash('Kunci lisensi sudah ada!', 'danger')
    
    return redirect(url_for('dashboard'))

@app.route('/delete/<license_key>')
def delete_license(license_key):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    execute_db('DELETE FROM licenses WHERE license_key = ?', [license_key])
    flash('Lisensi berhasil dihapus.', 'success')
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=5001, debug=True)