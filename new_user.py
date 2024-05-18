import os

module_dir = os.path.dirname(__file__)  # __file__ is a special variable of the module
path_to_players = os.path.join(module_dir, 'prompt_text/player_data/')

basic_character_yaml ="""character:
  health:
    max_health: 100
    current_health: 100
  stats:
    strength: 10
    agility: 8
  inventory:
    items: []
  skills:[]
  status_effects: []"""


###
import json

def maybe_create_new_player_file(user_id,user_name):
  """
  create a new character (with location and attributes/inventory yaml)
  but don't overwrite
  """
  with open('player2room.json','r') as f:
    player2room = json.load(f)
    if user_id not in player2room: ## new user
      with open('id2name.json','r') as f:
        id2name = json.load(f)
        id2name[user_id]=user_name
      with open('id2name.json','w') as f:
        json.dump(id2name,f)
      ## put in starting room
      with open('player2room.json','r') as f:
        player2room = json.load(f)
      player2room[user_id]="room0"
      with open('player2room.json','w') as f:
        json.dump(player2room,f)
      with open(path_to_players+user_id+".txt",'w') as f:
        f.write(basic_character_yaml)
      print("created character named %s" % user_id)
    else:
      print("continuing from %s I was" % user_id)

def main():
  print("creating player named test")
  create_new_player_file("test")

if __name__ == '__main__':
  main()

