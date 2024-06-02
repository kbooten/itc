import os

# dynamic path
module_dir = os.path.dirname(__file__)
path_to_prompts = os.path.join(module_dir, 'prompt_text')

from llm_interface import get_llm_response

def _get_contents_of_file(a_file):
    try:
        with open(a_file, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {a_file}: {e}")
        return ""

def _maybe_update(prompt, file):
    try:
        response_from_llm = get_llm_response(prompt)
        if "!same!" in response_from_llm.lower():
            return False
        else:
            with open(file, 'w') as f:
                print(f"Overwriting file {file}")
                f.write(response_from_llm)
            return True
    except Exception as e:
        print(f"Error updating file {file}: {e}")
        return False

def maybe_update_field_yaml(user_input, llm_response, history):
    try:
        file = "_field_yaml_.txt"
        field_yaml = _get_contents_of_file(file)
        prompt = _get_contents_of_file("field_yaml_rev_prompt.txt")
        prompt = prompt.replace('<<user_input>>', user_input)
        prompt = prompt.replace('<<llm_response>>', llm_response)
        prompt = prompt.replace('<<field_yaml>>', field_yaml)
        prompt = prompt.replace('<<history>>', history)
        return _maybe_update(prompt, file)
    except Exception as e:
        print(f"Error in maybe_update_field_yaml: {e}")
        return False

def maybe_update_field_prose(user_input, llm_response):
    try:
        file = "_field_prose_.txt"
        prompt = _get_contents_of_file("field_prose_rev_prompt.txt")
        field_prose = _get_contents_of_file("_field_prose_.txt")
        field_yaml = _get_contents_of_file("_field_yaml_.txt")
        prompt = prompt.replace('<<user_input>>', user_input)
        prompt = prompt.replace('<<llm_response>>', llm_response)
        prompt = prompt.replace('<<field_prose>>', field_prose)
        prompt = prompt.replace('<<field_yaml>>', field_yaml)
        return _maybe_update(prompt, file)
    except Exception as e:
        print(f"Error in maybe_update_field_prose: {e}")
        return False

def maybe_update_user_yaml(user_input, llm_response, user_yaml):
    try:
        with open("character_revision_prompt.txt", 'r') as f:
            prompt = f.read()
        prompt = prompt.replace('<<user_input>>', user_input)
        prompt = prompt.replace('<<llm_response>>', llm_response)
        prompt = prompt.replace('<<payload>>', user_yaml)
        response_from_llm = get_llm_response(prompt)
        if "!same!" in response_from_llm.lower():
            return user_yaml  # original
        else:
            return response_from_llm
    except Exception as e:
        print(f"Error in maybe_update_user_yaml: {e}")
        return user_yaml

def main():
    pass

if __name__ == '__main__':
    main()
