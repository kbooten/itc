import os
import json

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


def create_new_user(user_id,email):
  """
  create a new player with a character (with location and attributes/inventory yaml)
  but don't overwrite
  """
  ## new
  with open('id2email.json','r') as f:
    id2email = json.load(f)
  id2email[user_id]=email
  with open('id2email.json','w') as f:
    json.dump(id2email,f)
  ## new player location (set to none)
  with open('player2room.json','r') as f:
    player2room = json.load(f)
  player2room[user_id]=""
  with open('player2room.json','w') as f:
    json.dump(player2room,f)
  ## new player yaml
  with open(path_to_players+user_id+".txt",'w') as f:
    f.write(basic_character_yaml)


def main():
  print("creating player named test")
  create_new_player_file("test")


if __name__ == '__main__':
  main()