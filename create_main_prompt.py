import os
import json

# dynamic path
module_dir = os.path.dirname(__file__) 
path_to_prompts = os.path.join(module_dir, 'prompt_text')



from little_utilities import get_current_room_of_player


def get_main_prompt():
    with open(path_to_prompts+"/main_game_prompt.txt",'r') as f:
        main_prompt = f.read()
    return main_prompt


def get_current_room_text(room_id):
    with open(path_to_prompts+"/rooms/"+room_id+".txt",'r') as f:
        room_text = f.read()
    return room_text


def get_user_data(user_name):
    with open(path_to_prompts+"/player_data/"+user_name+".txt",'r') as f:
        user_data = f.read()
    return user_data


def build_prompt(user_input="what can I do?",user_name="test",room_id="room0"):
    main_prompt = get_main_prompt()
    room_id = get_current_room_of_player(user_name)
    room_text = get_current_room_text(room_id)
    user_data  =get_user_data(user_name)
    main_prompt = main_prompt.replace("<<room>>",room_text)
    main_prompt = main_prompt.replace("<<user_input>>",user_input)
    main_prompt = main_prompt.replace("<<player_data>>",user_data)
    return main_prompt


def main():
    print(build_prompt())


if __name__ == '__main__':
    main()