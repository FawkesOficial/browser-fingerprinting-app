from flask import Flask, request, jsonify, render_template
import os
import hashlib

app = Flask(__name__)

FINGERPRINT_FILE = "fingerprint_users.txt"


def load_fingerprints() -> dict:
    if not os.path.exists(FINGERPRINT_FILE):
        return {}
    with open(FINGERPRINT_FILE, "r") as f:
        return dict(line.strip().split(',', 1) for line in f)

def save_fingerprint(fingerprint, user_id) -> None:
    with open(FINGERPRINT_FILE, "a") as f:
        f.write(f"{fingerprint},{user_id}\n")


fingerprints = load_fingerprints()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log_fingerprint', methods=['POST'])
def log_fingerprint():
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400

    fingerprint_data = str(sorted(data.items()))
    fingerprint_hash = hashlib.sha256(fingerprint_data.encode()).hexdigest()

    if fingerprint_hash in fingerprints:
        user_id = fingerprints[fingerprint_hash]
    else:
        user_id = f"User#{len(fingerprints) + 1}"
        fingerprints[fingerprint_hash] = user_id
        save_fingerprint(fingerprint_hash, user_id)

    print(f"Received Fingerprint Data: {data}, Assigned ID: {user_id}")

    return jsonify({"status": "success", "user_id": user_id, "fingerprint": fingerprint_hash})

if __name__ == '__main__':
    app.run(debug=True)
