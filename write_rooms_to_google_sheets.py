from google_sheets_io import append_data_to_google_sheet

import json

import os

def get_current_room_desc(room_id):
	module_dir = os.path.dirname(__file__)  # __file__ is a special variable of the module
	path_to_rooms = os.path.join(module_dir, 'prompt_text/rooms/')
	with open(path_to_rooms+room_id+".txt",'r') as f:
		room_desc = f.read()
	return room_desc


def main():
	import time
	current_timestamp = int(time.time())

	# Load room information
	with open('room_id2room_title_author.json', 'r') as f:
	    room_id2title_author = json.load(f)
	print(room_id2title_author)


	room_info_to_write = [[current_timestamp, k, v["title"], v["author"], get_current_room_desc(k)] for k, v in room_id2title_author.items()]
	append_data_to_google_sheet(room_info_to_write,range_name='updated_rooms!A1')
	print("wrote rooms to google")




if __name__ == '__main__':
	main()

