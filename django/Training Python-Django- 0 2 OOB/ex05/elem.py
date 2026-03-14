
class Text(str):
	def __new__(cls, content=''):
		# Convertir a string por si es número u otro tipo
		content = str(content)

		# Escapar caracteres especiales de HTML
		content = content.replace('&', '&amp;')
		content = content.replace('<', '&lt;')
		content = content.replace('>', '&gt;')
		content = content.replace('"', '&quot;')

		# Reemplazar saltos de línea con <br />
		content = content.replace('\n', '\n<br />\n')

		# Crear la instancia de str
		return str.__new__(cls, content)


class Elem:
	def __init__(self, tag='div', attr=None, content=None, tag_type='double'):
		self.tag = tag
		self.attr = attr or {}
		self.tag_type = tag_type
		self.content = []

		# Si se proporciona contenido, agregarlo
		if content is not None:
			self.add_content(content)

	class ValidationError(Exception):
		pass

	def __str__(self):
		attr_str = ''
		for key, value in self.attr.items():
			attr_str += f' {key}="{value}"'

		if self.tag_type == 'simple':
			return f'<{self.tag}{attr_str} />'

		if not self.content:
			return f'<{self.tag}{attr_str}></{self.tag}>'

		content_lines = []
		for item in self.content:
			item_str = str(item)
			for line in item_str.split('\n'):
				content_lines.append('  ' + line)

		content_str = '\n' + '\n'.join(content_lines) + '\n'
		return f'<{self.tag}{attr_str}>{content_str}</{self.tag}>'

	def add_content(self, content):
		# Si es una lista, procesar cada elemento
		if isinstance(content, list):
			for item in content:
				# Validar que sea Text o Elem
				if not isinstance(item, (Text, Elem)):
					raise Elem.ValidationError(
						f"Content must be Text or Elem, got {type(item).__name__}"
					)
				# No agregar Text vacío
				if isinstance(item, Text) and str(item) == '':
					continue
				self.content.append(item)

		# Si es un item único
		elif isinstance(content, (Text, Elem)):
			# No agregar Text vacío
			if isinstance(content, Text) and str(content) == '':
				return
			self.content.append(content)

		# Si no es válido, lanzar excepción
		else:
			raise Elem.ValidationError(
				f"Content must be Text or Elem, got {type(content).__name__}"
			)

if __name__ == '__main__':
	title = Elem('title', content=Text('Hello ground!'))
	head = Elem('head', content=title)
	h1 = Elem('h1', content=Text('Oh no, not again!'))
	img = Elem('img', attr={'src': 'http://i.imgur.com/pfp3T.jpg'}, tag_type='simple')
	body = Elem('body', content=[h1, img])
	html = Elem('html', content=[head, body])
	print(html)



# <html>
#   <head>
#     <title>
#       "Hello ground!"
#     </title>
#   </head>
#   <body>
#     <h1>
#       "Oh no, not again!"
#     </h1>
#     <img src="http://i.imgur.com/pfp3T.jpg" />
#   </body>
# </html>
