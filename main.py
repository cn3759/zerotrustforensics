from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/papers')
def papers():
    return render_template('papers.html')

@app.route('/tampering')
def tampering():
    return render_template('tampering.html')

if __name__==("__main__"):
    #app.run(ssl_context='adhoc')
    app.run()