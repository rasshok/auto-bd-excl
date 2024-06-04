from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('auto_repair.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    requests = conn.execute('SELECT * FROM requests').fetchall()
    conn.close()
    return render_template('index.html', requests=requests)

@app.route('/add', methods=('GET', 'POST'))
def add_request():
    if request.method == 'POST':
        request_number = request.form['request_number']
        date_added = request.form['date_added']
        car_type = request.form['car_type']
        car_model = request.form['car_model']
        problem_description = request.form['problem_description']
        client_name = request.form['client_name']
        phone_number = request.form['phone_number']
        status = 'новая'

        conn = get_db_connection()
        conn.execute('INSERT INTO requests (request_number, date_added, car_type, car_model, problem_description, client_name, phone_number, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                     (request_number, date_added, car_type, car_model, problem_description, client_name, phone_number, status))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_request.html')

@app.route('/edit/<int:request_id>', methods=('GET', 'POST'))
def edit_request(request_id):
    conn = get_db_connection()
    request_data = conn.execute('SELECT * FROM requests WHERE id = ?', (request_id,)).fetchone()

    if request.method == 'POST':
        request_number = request.form['request_number']
        date_added = request.form['date_added']
        car_type = request.form['car_type']
        car_model = request.form['car_model']
        problem_description = request.form['problem_description']
        client_name = request.form['client_name']
        phone_number = request.form['phone_number']
        status = request.form['status']
        assigned_mechanic = request.form['assigned_mechanic']

        conn.execute('''
            UPDATE requests
            SET request_number = ?, date_added = ?, car_type = ?, car_model = ?, problem_description = ?, client_name = ?, phone_number = ?, status = ?, assigned_mechanic = ?
            WHERE id = ?
        ''', (request_number, date_added, car_type, car_model, problem_description, client_name, phone_number, status, assigned_mechanic, request_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_request.html', request=request_data)

@app.route('/delete/<int:request_id>', methods=('POST',))
def delete_request(request_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM requests WHERE id = ?', (request_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/upload', methods=('GET', 'POST'))
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            import_excel_to_db(file_path)
            os.remove(file_path)
            return redirect(url_for('index'))
    return render_template('upload.html')

def import_excel_to_db(file_path):
    df = pd.read_excel(file_path)
    conn = get_db_connection()
    for _, row in df.iterrows():
        conn.execute('INSERT INTO requests (request_number, date_added, car_type, car_model, problem_description, client_name, phone_number, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                     (row['request_number'], row['date_added'], row['car_type'], row['car_model'], row['problem_description'], row['client_name'], row['phone_number'], row['status']))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
