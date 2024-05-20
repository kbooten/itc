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

from little_utilities import get_current_room_of_player, look_up_email, update_player_room

import new_user 

from write_to_google_sheet import append_data_to_google_sheet

import time

import json


@auth.verify_password
def verify_password(meta_username, password):
    if meta_username in users and users[meta_username] == password:
        return meta_username


def process_input(user_text,user_id): ## this should be somewhere else!
    llm_response =  get_llm_response(build_prompt(user_text,user_id)) 
    #room = get_current_room_of_player(user_id)
    maybe_update_room(user_text,llm_response,room,user_id=user_id)
    maybe_update_character(user_text,llm_response,user_id)
    ## write to google
    append_data_to_google_sheet([[int(time.time()),user_id,look_up_email(user_id),user_text,llm_response]])
    return llm_response

rooms = ['Room1', 'Room2', 'Room3']


@app.route('/')
@auth.login_required
def home():
    return render_template('map.html', rooms=rooms)


@app.route('/select_room', methods=['POST'])
def select_room():
    room = request.form.get('room')
    user_id = request.form.get('user_id')
    if not room or not user_id:
        return "Missing room or user ID", 400
    update_player_room(user_id,room)
    return render_template('chat.html',room=room)


@app.route('/handshake', methods=['POST'])
def handshake():
    user_id = request.form.get('user_id')
    email = request.form.get('email')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    print(f'New user handshake: {user_id}')
    new_user.create_new_user(user_id,email)
    return jsonify({'message': 'Handshake successful', 'text': 'Welcome!'})


@app.route("/send_message", methods=["POST"])
def send_message():
    user_input = request.form.get("message")
    user_id = request.form.get("user_id")
    room = request.form.get("user_id")
    if user_input.strip() != "":
        response = process_input(user_input,user_id)
        return jsonify({"user": "Server", "text": response})  # Return only the server's response
    return jsonify({"error": "No message received"})


if __name__ == '__main__':
    app.run(debug=True)