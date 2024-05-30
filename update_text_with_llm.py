import os

# dynamic path
module_dir = os.path.dirname(__file__) 
path_to_prompts = os.path.join(module_dir, 'prompt_text')


from llm_interface import get_llm_response


def _get_contents_of_file(a_file):
    with open(a_file,'r') as f:
        payload = f.read()
    return payload


def _maybe_update(prompt,file):
    response_from_llm = get_llm_response(prompt)
    if "!same!" in response_from_llm.lower():  ## NEED TO MAKE MORE DURABLE
        return False
    else:
        with open(file,'w') as f:
            print("overwriting file %s" % file)
            f.write(response_from_llm)


def maybe_update_field_yaml(user_input,llm_response,history):
    file = "_field_yaml_.txt"
    field_yaml = _get_contents_of_file(file)
    prompt = _get_contents_of_file("field_yaml_rev_prompt.txt")
    prompt = prompt.replace('<<user_input>>',user_input)
    prompt = prompt.replace('<<llm_response>>',llm_response)
    prompt = prompt.replace('<<field_yaml>>',field_yaml)
    prompt = prompt.replace('<<history>>',field_yaml)
    return _maybe_update(prompt,file)


def maybe_update_field_prose(user_input,llm_response):
    file = "_field_prose_.txt"
    prompt = _get_contents_of_file("field_prose_rev_prompt.txt")
    field_prose = _get_contents_of_file("_field_prose_.txt")
    field_yaml = _get_contents_of_file("_field_yaml_.txt")
    prompt = prompt.replace('<<user_input>>',user_input)
    prompt = prompt.replace('<<llm_response>>',llm_response)
    prompt = prompt.replace('<<field_prose>>',field_prose)
    prompt = prompt.replace('<<field_yaml>>',field_yaml)
    return _maybe_update(prompt,file)


def maybe_update_user_yaml(user_input, llm_response, user_yaml):
    with open("character_revision_prompt.txt",'r') as f:
        prompt = f.read()
    prompt = prompt.replace('<<user_input>>>',user_input)
    prompt = prompt.replace('<<llm_response>>',llm_response)
    prompt = prompt.replace('<<payload>>',user_yaml)
    response_from_llm = get_llm_response(prompt)
    if "!same!" in response_from_llm.lower():
        return user_yaml ## original
    else:
        return response_from_llm


def main():
    pass

if __name__ == '__main__':
    main()