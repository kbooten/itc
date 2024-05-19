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

with open('id2name.json','r') as f:
    id2player = json.load(f)

def replace_player_id_with_name(text):
    for player_id in id2player:
        text = text.replace(player_id,"[USER:%s]" % id2player[player_id])
    return text

    
