import json

def update_player_room(user_id,room):
    with open('player2room.json','r') as f:
        player2room = json.load(f)
    player2room[user_id]=room
    with open('player2room.json','w') as f:
        json.dump(player2room,f)

def look_up_email(user_id):
    with open('id2email.json','r') as f:
        id2email = json.load(f)
    return id2email[user_id]

def get_room_author_title(room_id):
    with open('room_id2room_title_author.json','r') as f:
        room_id2room_title_author = json.load(f)
    return room_id2room_title_author[room_id]

def room_player_is_in(user_id):
    with open('player2room.json','r') as f:
        player2room = json.load(f)
    if user_id in player2room:
        return player2room[user_id]
    else:
        return None


import os


def user_id2yaml(user_id):
    module_dir = os.path.dirname(__file__)  # __file__ is a special variable of the module
    path_to_players = os.path.join(module_dir, 'prompt_text/player_data/')
    with open(path_to_players+user_id+".txt",'r') as f:
        yaml = f.read()
    return yaml