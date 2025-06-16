import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pathlib import Path

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Path to the applications file
DATA_FILE = Path("applications.json")

# Ensure the file exists with a default empty list
if not DATA_FILE.exists():
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

# Load applications safely from the file


def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

# Save applications back to the file


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


# Endpoint to handle job applications
@app.route('/')
def home():
    return render_template('index.html')


@app.route("/admin")
def admin():
    return render_template('admin.html')


@app.route('/apply', methods=['POST'])
def apply():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["full_name", "email", "phone", "position"]
    for field in required_fields:
        if field not in data or not data[field].strip():
            return jsonify({"error": f"Missing required field: {field}"}), 400

    print("\n✅ New Job Application Received:")
    print(json.dumps(data, indent=2))

    applications = load_data()
    applications.append(data)
    save_data(applications)

    return jsonify({
        "message": "Application submitted successfully!",
        "applicant": data["full_name"]
    }), 200

# Admin route to view all submitted applications


@app.route('/admin/applications', methods=['GET'])
def get_applications():
    applications = load_data()
    return jsonify(applications), 200


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
