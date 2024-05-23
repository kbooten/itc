import json

from google_sheets_io import read_rooms_from_google_sheet

import os


# dynamic path
module_dir = os.path.dirname(__file__) 
path_to_prompts = os.path.join(module_dir, 'prompt_text/rooms/')


#path_to_users = os.path.join(module_dir, 'prompt_text/player_data/')

#[x[0] for x in os.walk(directory)]

# os.mkdir(path_to_prompts)
# os.mkdir(path_to_users)
# os.makedirs(path_to_prompts, exist_ok=True)
# os.makedirs(path_to_users, exist_ok=True)


room_yaml = """public_description: >
  <<public>>. 
secret_description: >
  <<private>>."""

style_temp= """

In responding to the user, it is very important that you obey these stylistic commands:

<<style>>


"""

imit_temp="""

In responding to the user, you should try your best to imitate the following sample of text:

"<<imit>>"


"""

backup="""
Respond in an interesting, detailed, and not-corny way. When in doubt, be reserved, sticking only to the description of physical details.
Don't try to make things sound too fun.  Try to be objective and literal.
"""

def build_style_instruction(style,imit,backup=backup):
	if style!=None and imit!=None:
		to_return = style_temp.replace("<<style>>",style)
		to_return += imit_temp.replace("<<imit>>",imit)
		return to_return
	if style!=None:
		return style_temp.replace("<<style>>",style)
	if imit!=None:
		return imit_temp.replace("<<imit>>",imit)
	else:
		return backup

def build_room_description(public,private):
	return room_yaml.replace("<<public>>",public).replace("<<private>>",private)



def build_rooms():
	"""
	builds rooms and returns list of their ids
	"""
	room_data = read_rooms_from_google_sheet()


	room_id2room_title_author = {}

	for n,r in enumerate(room_data):
		desired_data_length = 6
		r = [field if field!="" else None for field in r]
		r = r + [None] * (desired_data_length - len(r))
		author,title,public_desc,private_desc,style_desc,to_mimic = r
		room_id = 'room'+str(n)
		room_id2room_title_author[room_id]={"title":title,"author":author}
		with open(path_to_prompts+room_id+".txt",'w') as f:
			f.write(build_room_description(public_desc,private_desc))
		with open(path_to_prompts+room_id+"_voice.txt",'w') as f:
			f.write(build_style_instruction(style_desc,to_mimic))
		##

	with open('room_id2room_title_author.json','w') as f:
		json.dump(room_id2room_title_author,f)

	# return room_id2room_title_author.keys() 


def main():
	build_rooms()

if __name__ == '__main__':
	main()






