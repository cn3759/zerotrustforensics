import datetime
import sqlite3
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)

ids = ['AT-1', 'AT-2', 'AB-1', 'AB-2', 'AB-3', 'AB-4']

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_feature(feature_id):
    conn = get_db_connection()
    feature = conn.execute('SELECT * from features WHERE id = ?', (feature_id,)).fetchone()
    conn.close()
    if feature is None:
        abort(404)
    return feature

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/papers')
def papers():
    return render_template('papers.html')

@app.route('/tampering')
def tampering():
    return render_template('tampering.html')

@app.route('/tampering_features')
def tampering_features():
    conn = get_db_connection()
    features = conn.execute('SELECT * from features ORDER by ID DESC').fetchall()
    conn.close()
    return render_template('tampering_features.html', features=features)

@app.route('/add_feature', methods=('GET', 'POST'))
def add_feature():
    if request.method == 'POST':
        print(request.form)
        description = request.form['description']
        reference = request.form['reference']
        feature_map = {}
        for id in ids:
            try:
                if request.form[id]:
                    feature_map[id] = 1
            except:
                feature_map[id] = 0
        conn = get_db_connection()
        conn.execute('INSERT INTO features (created, Description, Reference, "AT-1", "AT-2", "AB-1", "AB-2", "AB-3", '
                     '"AB-4") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (datetime.datetime.now(), description,
                                                                 reference, feature_map['AT-1'], feature_map['AT-2'],
        feature_map['AB-1'], feature_map['AB-2'], feature_map['AB-3'], feature_map['AB-4']))
        conn.commit()
        conn.close()
        return redirect(url_for('tampering_features'))
    return render_template('add_feature.html')

@app.route('/<int:feature_id>')
def feature(feature_id):
    feature = get_feature(feature_id)
    return render_template('display_feature.html', feature=feature)

if __name__==("__main__"):
    #app.run(ssl_context=('certs/cert.pem', 'certs/privkey.pem'))
    #app.run(host='0.0.0.0', port='443', ssl_context=('certs/cert.pem', 'certs/privkey.pem'))
    app.run(host='0.0.0.0', port='80')
    #app.run()