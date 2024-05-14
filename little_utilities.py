import json

def get_current_room_of_player(user_name):
    with open('player2room.json','r') as f:
        player2room = json.load(f)
    return player2room[user_name]
