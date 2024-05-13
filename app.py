from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


from create_main_prompt import build_prompt

users = {
    "itc": "plats",
}

from llm_interface import get_llm_response

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

def process_input(user_text,user_name):
    llm_response =  get_llm_response(build_prompt(user_text,user_name))

@app.route("/", methods=["GET"])
@auth.login_required
def index():
    return render_template("index.html")  # Initial page load

@app.route("/send_message", methods=["POST"])
def send_message():
    user_input = request.form.get("message")
    user_id = request.form.get("user_id")
    room_id = request.form.get("room_id") 
    if user_input.strip() != "":
        response = process_input(user_input,user_id)
        return jsonify({"user": "Server", "text": response})  # Return only the server's response
    return jsonify({"error": "No message received"})

if __name__ == '__main__':
    app.run(debug=True)
