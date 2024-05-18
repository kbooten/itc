import os

# dynamic path
module_dir = os.path.dirname(__file__) 
path_to_prompts = os.path.join(module_dir, 'prompting/prompt_text')


from llm_interface import get_llm_response


# def fill_out_prompt(prompt,user_input,llm_response,payload,user_id=None):
#     prompt = prompt.replace('<<user_input>>>',user_input)
#     prompt = prompt.replace('<<llm_response>>',llm_response)
#     prompt = prompt.replace('<<payload>>',payload)
#     if user_id!=None:
#         prompt = prompt.replace('<<user_id>>',user_id)
#     return prompt

def _get_contents_of_file(a_file):
    with open(a_file,'r') as f:
        payload = f.read()
    return payload

def _maybe_update(prompt,file,debug=False):
    response_from_llm = get_llm_response(prompt)
    if "!same!" in response_from_llm.lower():  ## NEED TO MAKE MORE DURABLE
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
                        debug=False,
                        user_id=None):
    file = path_to_prompts+"/rooms/"+room+".txt"
    payload = _get_contents_of_file(file)
    with open(path_to_prompts+"/room_revision_prompt.txt",'r') as f:
        prompt = f.read()
    prompt = prompt.replace('<<user_input>>',user_input)
    prompt = prompt.replace('<<llm_response>>',llm_response)
    prompt = prompt.replace('<<payload>>',payload)
    if user_id!=None:
        prompt = prompt.replace('<<user_id>>',user_id)
    print(prompt)
    _maybe_update(prompt,file,debug=debug)


def maybe_update_character(  user_input="grab Pavioni lever espresso machine and place it in my bag",
                            llm_response="You take the espresso machine.",
                            user_name="test",
                            debug=False):
    file = path_to_prompts+"/player_data/"+user_name+".txt"
    payload = _get_contents_of_file(file)
    with open(path_to_prompts+"/character_revision_prompt.txt",'r') as f:
        prompt = f.read()
    prompt = prompt.replace('<<user_input>>>',user_input)
    prompt = prompt.replace('<<llm_response>>',llm_response)
    prompt = prompt.replace('<<payload>>',payload)
    _maybe_update(prompt,file,debug=debug)


def main():
    maybe_update_room(debug=True)
    maybe_update_character(debug=True)


if __name__ == '__main__':
    main()

