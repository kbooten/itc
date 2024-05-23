import json
import os
import glob



def remove_user_files():
	# Specify the directory and the suffix of the files to delete
	module_dir = os.path.dirname(__file__)  # __file__ is a special variable of the module
	path_to_players = os.path.join(module_dir, 'prompt_text/player_data/')
	
	directory = '/prompt_text/player_data/'
	suffix = '.txt'  # Example suffix

	# Create the pattern to match files with the specified suffix
	pattern = os.path.join(path_to_players, '*' + suffix)

	# Use glob to find all files that match the pattern
	files_to_delete = glob.glob(pattern)

	# Delete each file found
	for file_path in files_to_delete:
	    try:
	        os.remove(file_path)
	        print(f"Deleted: {file_path}")
	    except Exception as e:
	        print(f"Error deleting {file_path}: {e}")


def remove_room_files():
	# Specify the directory and the suffix of the files to delete
	module_dir = os.path.dirname(__file__)  # __file__ is a special variable of the module
	path_to_rooms = os.path.join(module_dir, 'prompt_text/rooms/')
	
	suffix = '.txt'  # Example suffix

	# Create the pattern to match files with the specified suffix
	pattern = os.path.join(path_to_rooms, '*' + suffix)

	# Use glob to find all files that match the pattern
	files_to_delete = glob.glob(pattern)

	# Delete each file found
	for file_path in files_to_delete:
	    try:
	        os.remove(file_path)
	        print(f"Deleted: {file_path}")
	    except Exception as e:
	        print(f"Error deleting {file_path}: {e}")


def reinit():

	with open('id2email.json','w') as f:
		json.dump({},f)

	with open('player2room.json','w') as f:
		json.dump({},f)

	with open('room_id2room_title_author.json','w') as f:
		json.dump({},f)

	remove_user_files()
	remove_room_files()


def main():
	reinit()




if __name__ == '__main__':
	main()