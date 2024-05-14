import json

def get_current_room_of_player(user_name):
    with open('player2room.json','r') as f:
        player2room = json.load(f)
    return player2room[user_name]

def update_player_room(user_name,room):
    with open('player2room.json','r') as f:
        player2room = json.load(f)
    player2room[user_name]=room
    with open('player2room.json','w') as f:
        json.dump(player2room,f)
