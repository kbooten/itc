from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

users = {
    "itc": "platsplatsplats",
}

from llm_interface import get_llm_response

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

messages = []

def process_input(text):
    return get_llm_response(text)

@app.route("/", methods=["GET"])
@auth.login_required
def index():
    return render_template("index.html")  # Initial page load

@app.route("/send_message", methods=["POST"])
def send_message():
    user_input = request.form.get("message")
    if user_input.strip() != "":
        messages.append({"user": "You", "text": user_input})
        response = process_input(user_input)
        messages.append({"user": "Server", "text": response})
        return jsonify({"user": "Server", "text": response})  # Return only the server's response
    return jsonify({"error": "No message received"})


if __name__ == '__main__':
    app.run(debug=True)
