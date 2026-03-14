from elem import Elem, Text
from elements import *


class Page:
	def __init__(self, root):
		if not isinstance(root, Elem):
			raise ValueError("root debe ser una instancia de Elem")
		self.root = root

	def __str__(self):
		html_str = str(self.root)
		if self.root.tag == 'html':
			return '<!DOCTYPE html>\n' + html_str
		return html_str

	def write_to_file(self, filename):

		with open(filename, 'w', encoding='utf-8') as f:
			f.write(str(self))

	def is_valid(self):

		# TODO: Implementar validación
		return True
