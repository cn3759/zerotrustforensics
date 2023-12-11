import sqlite3
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)

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
    features = conn.execute('SELECT * from features').fetchall()
    conn.close()
    return render_template('tampering_features.html', features=features)

@app.route('/add_feature', methods=('GET', 'POST'))
def add_feature():
    if request.method == 'POST':
        description = request.form['description']
        print(description)
        return redirect(url_for('add_feature'))
    return render_template('add_feature.html')

@app.route('/<int:feature_id>')
def feature(feature_id):
    feature = get_feature(feature_id)
    return render_template('display_feature.html', feature=feature)

if __name__==("__main__"):
    app.run(ssl_context=('certs/cert.pem', 'certs/privkey.pem'))
    #app.run(host='0.0.0.0', port='443', ssl_context=('certs/cert.pem', 'certs/privkey.pem                                                                   '))
    #app.run()