import os

module_dir = os.path.dirname(__file__)  # __file__ is a special variable of the module
path_to_players = os.path.join(module_dir, 'prompting/prompt_text/player_data/')

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

def create_new_player_file(player_name):
  with open(path_to_players+player_name+".txt",'w') as f:
    f.write(basic_character_yaml)
  ## put in starting room
  with open('player2room.json','r') as f:
    player2room = json.load(f)
  player2room[player_name]="room0"
  with open('player2room.json','w') as f:
    json.dump(player2room,f)

def main():
  print("creating player named test")
  create_new_player_file("test")

if __name__ == '__main__':
  main()

