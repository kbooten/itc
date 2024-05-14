import os

# dynamic path
module_dir = os.path.dirname(__file__) 
path_to_prompts = os.path.join(module_dir, 'prompting/prompt_text')
with open(path_to_prompts+"/room_movement_prompt.txt","r") as f:
    prompt = f.read()

from llm_interface import get_llm_response

from little_utilities import get_current_room_of_player,update_player_room


def fill_out_prompt(prompt,user_input,llm_response,payload):
    prompt = prompt.replace('<<user_input>>>',user_input)
    prompt = prompt.replace('<<llm_response>>',llm_response)
    prompt = prompt.replace('<<payload>>',payload)
    return prompt


def maybe_move_to_new_room(user_name,user_input,llm_response,debug=False):
    room = get_current_room_of_player(user_name)
    ## room description is payload
    file = path_to_prompts+"/rooms/"+room+".txt"
    with open(file,'r') as f:
        payload = f.read()    
    prompt_filled = fill_out_prompt(prompt,user_input,llm_response,payload) 
    response_from_llm = get_llm_response(prompt_filled)
    print(response_from_llm)
    if "!same!" in response_from_llm.lower():
        pass
    else:
        if debug==False:
            update_player_room(user_name,response_from_llm)
        else:
            print("%s is now in %s" % (user_name,response_from_llm))


def main():
    maybe_move_to_new_room('test',"I open the door.","You walk through the door.",debug=True)


if __name__ == '__main__':
    main()
