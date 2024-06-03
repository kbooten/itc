from google_sheets_io import append_data_to_google_sheet

import json

import time

def current_field():
	with open("_field_prose_.txt","r") as f:
		return f.read()

def current_field_yaml():
	with open("_field_yaml_.txt","r") as f:
		return f.read()


def write():
	spatial_info_to_write = [[int(time.time()), current_field(), current_field_yaml()]] ## timestamp, field description, map
	append_data_to_google_sheet(spatial_info_to_write,range_name='field!A1')
	print("wrote spatial description + map to google")


def main():
	write()

if __name__ == '__main__':
	main()

