from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/test-login', methods=['POST'])
def test_login():
    try:
        # Debugging: Print request data
        print("Request received:", request.form)

        if 'username' not in request.form or 'password' not in request.form:
            return jsonify({"error": "Missing username or password"}), 400

        username = request.form['username']
        password = request.form['password']

        # Run Selenium script with Python3 (fix subprocess issue)
        result = subprocess.run(
            ["python3", "selenium_script.py", username, password],
            capture_output=True,
            text=True
        )

        return jsonify({"output": result.stdout})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
