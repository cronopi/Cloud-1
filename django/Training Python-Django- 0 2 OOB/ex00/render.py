import sys
import os
import re

def validate_arguments():
	if len(sys.argv) != 2:
		print("wrong number of arguments")
		return None
	return sys.argv[1]

def validate_extension(filename):
	if not filename.endswith(".template"):
		print("wrong file extension")
		return False
	return True

def read_template(filename):
	if not os.path.isfile(filename):
		print("file does not exist")
		return None
	with open(filename, 'r') as file:
			content = file.read()
	return content

def load_settings():
	settings = {}
	if not os.path.isfile("settings.py"):
		print("settings.py file does not exist")
		return None

	with open("settings.py", 'r') as file:
		content = file.read()

		exec(content, settings)
		settings = {k: v for k, v in settings.items() if not k.startswith('__')}

		return settings

def replace_placeholders(content, settings):
	try:
		result = content.format(**settings)
		return result
	except Exception as e:
		print(f"Error replacing variables: {e}")
		return None

def write_html(filename, rendered_content):
	html_filename = filename.replace('.template', '.html')

	try:
		with open(html_filename, 'w') as file:
			file.write(rendered_content)
		return True
	except Exception as e:
		print(f"Error writing HTML file: {e}")
		return False

if __name__ == "__main__":
	filename = validate_arguments()
	if filename is None:
		sys.exit(1)

	if not validate_extension(filename):
		sys.exit(1)

	content = read_template(filename)
	if content is None:
		sys.exit(1)

	settings = load_settings()
	if settings is None:
		sys.exit(1)

	rendered = replace_placeholders(content, settings)
	if rendered is None:
		sys.exit(1)

	if not write_html(filename, rendered):
		sys.exit(1)
