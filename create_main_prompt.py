import os
import json

# dynamic path
module_dir = os.path.dirname(__file__) 
path_to_prompts = os.path.join(module_dir, 'prompt_text')


def get_main_prompt():
    with open(path_to_prompts+"/main_game_prompt.txt",'r') as f:
        main_prompt = f.read()
    return main_prompt


def get_current_room_text(room_id):
    with open(path_to_prompts+"/rooms/"+room_id+".txt",'r') as f:
        room_text = f.read()
    return room_text

def get_current_room_text_voice(room_id):
    with open(path_to_prompts+"/rooms/"+room_id+"_voice.txt",'r') as f:
        room_voice = f.read()
    return room_voice


def get_user_data(user_name):
    with open(path_to_prompts+"/player_data/"+user_name+".txt",'r') as f:
        user_data = f.read()
    return user_data


def build_prompt(user_input="what can I do?",user_name="test",room_id="room0"):
    main_prompt = get_main_prompt()
    room_text = get_current_room_text(room_id)
    room_voice = get_current_room_text_voice(room_id)
    user_data  =get_user_data(user_name)
    main_prompt = main_prompt.replace("<<room>>",room_text)
    main_prompt = main_prompt.replace("<<room_voice>>",room_voice)
    main_prompt = main_prompt.replace("<<player_data>>",user_data)
    main_prompt = main_prompt.replace("<<user_input>>",user_input)
    main_prompt = main_prompt.replace("<<player_data>>",user_data)
    print(main_prompt)
    return main_prompt


def main():
    print(build_prompt())


if __name__ == '__main__':
    main()