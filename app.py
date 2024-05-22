from flask import Flask, render_template, request, jsonify
from flask_httpauth import HTTPBasicAuth
import json
import time

import threading ## for rewriting 

from create_main_prompt import build_prompt
from llm_interface import get_llm_response
from update_text_with_llm import maybe_update_room, maybe_update_character, maybe_remove_person_from_room
from little_utilities import look_up_email, update_player_room, get_room_author_title, room_player_is_in
import new_user 
from google_sheets_io import append_data_to_google_sheet
import building_rooms


app = Flask(__name__)
auth = HTTPBasicAuth()


# Users for basic auth
users = {
    "itc": "platsplatsplats",  # remember to remove this
} 


# Load room information
with open('room_id2room_title_author.json', 'r') as f:
    room_id2title_author = json.load(f)


room_info_for_frontend = [
    {"id": k, "title": v["title"], "author": v["author"]}
    for k, v in room_id2title_author.items()
]


@auth.verify_password
def verify_password(meta_username, password):
    if meta_username in users and users[meta_username] == password:
        return meta_username
    return None


def process_input(user_text, user_id, room_id):
    """
    get main llm response
    threadedly start other changes to castle
    return main llm response
    """
    llm_response = get_llm_response(build_prompt(user_text, user_id, room_id))
    thread = threading.Thread(target=process_input_slow_stuff, args=(user_text, user_id, room_id, llm_response))
    thread.start()
    return llm_response


def process_input_slow_stuff(user_text, user_id, room_id, llm_response):
    """
    to be threaded so costly io and llm responses that won't be immediately returned 
    won't block return of response
    """
    maybe_update_room(user_text, llm_response, room_id)
    char_was_updated = maybe_update_character(user_text, llm_response, user_id) ## bool, True means updated
    data_to_append = [[int(time.time()), user_id, look_up_email(user_id), 
        user_text, llm_response, room_id, room_id2title_author[room_id]['title']]]
    append_data_to_google_sheet(data_to_append)


@app.route('/')
@auth.login_required
def home():
    return render_template('map.html', rooms=room_info_for_frontend)


@app.route('/select_room', methods=['POST'])
def select_room():
    room = request.form.get('room_id')
    user_id = request.form.get('user_id')
    if not room or not user_id:
        return "Missing room or user ID", 400
    prev_room = room_player_is_in(user_id)
    print(prev_room)
    print(type(prev_room))
    ## maybe remove user from prev room
    if type(prev_room)==str:
        if prev_room!=room:
            maybe_remove_person_from_room(user_id,prev_room)
    ##
    update_player_room(user_id, room)
    ##
    author_title_json = get_room_author_title(room)
    room_author,room_title=author_title_json['author'],author_title_json['title']
    return render_template('chat.html', room_info={"id": room, "title": room_title, "author": room_author})


@app.route('/handshake', methods=['POST'])
def handshake():
    user_id = request.form.get('user_id')
    email = request.form.get('email')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    print(f'New user handshake: {user_id}')
    new_user.create_new_user(user_id, email)
    return jsonify({'message': 'Handshake successful', 'text': 'Welcome!'})


@app.route('/fetch_user_data', methods=['POST'])
def fetch_user_data():
    user_id = request.form.get('user_id')

    return user_id

@app.route("/send_message", methods=["POST"])
def send_message():
    user_input = request.form.get("message")
    user_id = request.form.get("user_id")
    room_id = request.form.get("room_id")
    if user_input.strip():
        response = process_input(user_input, user_id, room_id)
        return jsonify({"user": "Server", "text": response})
    return jsonify({"error": "No message received"})


if __name__ == '__main__':
    app.run(debug=True)