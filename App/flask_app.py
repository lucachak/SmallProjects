# flask_app.py (place this in your project root)
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Sample data
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
]

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the API",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/v1/status')
def status():
    return jsonify({
        "status": "healthy",
        "uptime": "running",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/api/v1/data', methods=['POST'])
def post_data():
    data = request.get_json()
    return jsonify({
        "message": "Data received",
        "data": data,
        "timestamp": datetime.now().isoformat()
    }), 201

@app.route('/api/v1/delete', methods=['DELETE'])
def delete_data():
    return jsonify({
        "message": "Resource deleted",
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    print("Starting Flask server...")
    print(f"Server will be available at http://localhost:5000")
    app.run(debug=False, host='localhost', port=5000, use_reloader=False)
