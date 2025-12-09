#!/home/lucas/Documents/Python/Automation/.venv/bin/python3 Api
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn’t need to be reachable, just forces choosing an interface
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

app = Flask(__name__)


# Configuração do banco (pode ser SQLite, PostgreSQL, MySQL etc.)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


items = [
        {"id":1, "name":"Sample item 1"},
        {"id":2, "name":"Sample item 2"}
        ]

@app.route("/")
def index():
    return render_template("index.html", items=items)


@app.route("/create", methods=['POST'])
def create():

    new_item = request.form.get('item_name')

    if new_item:
        new_id = max(item['if'] for item in items) + 1 if items else 1 
        new_item = {"id":new_id, "name":new_item}
        items.append(new_item)

    return redirect(url_for('index'))

@app.route('/update/<int:item_id>', methods=['POST'])
def update(item_id):
    """Handles updating an existing item."""
    updated_name = request.form.get('updated_name')

    for item in items:
        if item['id'] == item_id:
            item['name'] = updated_name
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    """Handles deleting an item."""
    
    global items
    items = [item for item in items if item['id'] != item_id]
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
