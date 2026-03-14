from elem import Elem, Text

class Html(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('html', attr=attr, content=content, tag_type='double')

class Head(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('head', attr=attr, content=content, tag_type='double')

class Body(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('body', attr=attr, content=content, tag_type='double')

class Title(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('title', attr=attr, content=content, tag_type='double')

class Meta(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('meta', attr=attr, content=content, tag_type='simple')

class Img(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('img', attr=attr, content=content, tag_type='simple')

class Table(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('table', attr=attr, content=content, tag_type='double')

class Th(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('th', attr=attr, content=content, tag_type='double')

class Tr(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('tr', attr=attr, content=content, tag_type='double')

class Td(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('td', attr=attr, content=content, tag_type='double')

class Ul(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('ul', attr=attr, content=content, tag_type='double')

class Ol(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('ol', attr=attr, content=content, tag_type='double')

class Li(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('li', attr=attr, content=content, tag_type='double')

class H1(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('h1', attr=attr, content=content, tag_type='double')

class H2(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('h2', attr=attr, content=content, tag_type='double')

class P(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('p', attr=attr, content=content, tag_type='double')

class Div(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('div', attr=attr, content=content, tag_type='double')

class Span(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('span', attr=attr, content=content, tag_type='double')

class Hr(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('hr', attr=attr, content=content, tag_type='simple')

class Br(Elem):
	def __init__(self, content=None, **attr):
		super().__init__('br', attr=attr, content=content, tag_type='simple')


if __name__ == '__main__':
	# Comprehensive test with all classes
	doc = Html([
		Head([
			Title(Text("My Website")),
			Meta(name="charset", charset="UTF-8")
		]),
		Body([
			H1(Text("Welcome to My Site")),
			H2(Text("Introduction")),
			P(Text("This is a page with all HTML elements.")),
			Div([
				Span(Text("Important text")),
				Br(),
				Img(src="http://i.imgur.com/pfp3T.jpg", alt="Example image"),
				Hr()
			]),
			Ul([
				Li(Text("Item 1")),
				Li(Text("Item 2")),
				Li(Text("Item 3"))
			]),
			Ol([
				Li(Text("First")),
				Li(Text("Second")),
				Li(Text("Third"))
			]),
			Table([
				Tr([
					Th(Text("Name")),
					Th(Text("Value"))
				]),
				Tr([
					Td(Text("Python")),
					Td(Text("Programming Language"))
				]),
				Tr([
					Td(Text("HTML")),
					Td(Text("Markup Language"))
				])
			])
		])
	])

	print(doc)
