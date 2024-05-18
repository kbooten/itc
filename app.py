from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


from create_main_prompt import build_prompt

users = {
    "itc": "platsplatsplats", ### remember to nix
} 

from llm_interface import get_llm_response

from update_text_with_llm import maybe_update_room, maybe_update_character

from move_to_new_room import maybe_move_to_new_room

from little_utilities import get_current_room_of_player

import new_user 

from write_to_google_sheet import append_data_to_google_sheet

import time

import json


@auth.verify_password
def verify_password(meta_username, password):
    if meta_username in users and users[meta_username] == password:
        return meta_username

def process_input(user_text,user_id): ## this should be somewhere else!
    llm_response =  get_llm_response(build_prompt(user_text,user_id)) ## this will create a new user but should refactor
    room = get_current_room_of_player(user_id)
    maybe_update_room(user_text,llm_response,room,user_id=user_id)
    maybe_update_character(user_text,llm_response,user_id)
    maybe_move_to_new_room(user_id,user_text,llm_response)
    ## write to google
    with open('id2name.json','r') as f:
        id2name = json.load(f)
    append_data_to_google_sheet([[int(time.time()),user_id,id2name[user_id],user_text,llm_response]])
    return llm_response

@app.route("/", methods=["GET"])
@auth.login_required
def index():
    return render_template("index.html")  # Initial page load

@app.route("/handshake", methods=["POST"])
def handshake():
    user_id = request.form.get("user_id")
    user_name = request.form.get("user_name")
    new_user.maybe_create_new_player_file(user_id,user_name)
    response = process_input("Could you please tell me where I am and what I should do?",user_id)
    return jsonify({"user": "Server", "text": response})  # Return only the server's response
    return jsonify({"error": "No message received"})

@app.route("/send_message", methods=["POST"])
def send_message():
    user_input = request.form.get("message")
    user_id = request.form.get("user_id")
    if user_input.strip() != "":
        response = process_input(user_input,user_id)
        return jsonify({"user": "Server", "text": response})  # Return only the server's response
    return jsonify({"error": "No message received"})

if __name__ == '__main__':
    app.run(debug=True)