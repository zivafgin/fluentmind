from flask import Flask, render_template, url_for
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Pass datetime to the template context
    return render_template('lan_practice.html', datetime=datetime)

if __name__ == '__main__':
    app.run(debug=True)
