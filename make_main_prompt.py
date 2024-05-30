import os
import json

def get_main_prompt():
    with open("main_game_prompt.txt",'r') as f:
        main_prompt = f.read()
    return main_prompt



def build_prompt(user_input="what can I do?",user_yaml="data", history=""):
    with open("main_game_prompt.txt",'r') as f:
        main_prompt = f.read()
    with open('_field_yaml_.txt') as f:
        field_yaml = f.read()
    with open('_field_prose_.txt') as f:
        field_prose = f.read()
    main_prompt = main_prompt.replace("<<field_yaml>>",field_yaml)
    main_prompt = main_prompt.replace("<<field_prose>>",field_prose)
    main_prompt = main_prompt.replace("<<player_input>>",user_input)
    main_prompt = main_prompt.replace("<<player_yaml>>",user_yaml)
    main_prompt = main_prompt.replace("<<history>>",history)
    print(main_prompt)
    return main_prompt


def main():
    print(build_prompt())


if __name__ == '__main__':
    main()