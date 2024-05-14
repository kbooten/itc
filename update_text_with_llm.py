import os

# dynamic path
module_dir = os.path.dirname(__file__) 
path_to_prompts = os.path.join(module_dir, 'prompting/prompt_text')


from llm_interface import get_llm_response


def fill_out_prompt(prompt,user_input,llm_response,payload):
    prompt = prompt.replace('<<user_input>>>',user_input)
    prompt = prompt.replace('<<llm_response>>',llm_response)
    prompt = prompt.replace('<<payload>>',payload)
    return prompt


def _maybe_update(user_input,llm_response,prompt,file,debug=False):
    with open(file,'r') as f:
        payload = f.read()
    prompt = fill_out_prompt(prompt,user_input,llm_response,payload)
    response_from_llm = get_llm_response(prompt)
    if "!same!" in response_from_llm:
        pass
    else:
        if debug==True:
            print(response_from_llm)
        else:
            with open(file,'w') as f:
                print("overwriting file %s" % file)
                f.write(response_from_llm)

def maybe_update_room(   user_input="grab Pavioni lever espresso machine and place it in my bag",
                        llm_response="You take the espresso machine.",
                        room="room0",
                        debug=False):
    file = path_to_prompts+"/rooms/"+room+".txt"
    with open(path_to_prompts+"/room_revision_prompt.txt",'r') as f:
        prompt = f.read()
    _maybe_update(user_input,llm_response,prompt,file,debug=debug)


def maybe_update_character(  user_input="grab Pavioni lever espresso machine and place it in my bag",
                            llm_response="You take the espresso machine.",
                            user_name="test",
                            debug=False):
    file = path_to_prompts+"/player_data/"+user_name+".txt"
    with open(path_to_prompts+"/character_revision_prompt.txt",'r') as f:
        prompt = f.read()
    _maybe_update(user_input,llm_response,prompt,file,debug=debug)


def main():
    maybe_update_room(debug=True)
    maybe_update_character(debug=True)


if __name__ == '__main__':
    main()

