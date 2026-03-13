from elem import Elem, Text

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

title = Elem('title', content=Text('Hello ground!'))
head = Elem('head', content=title)
h1 = Elem('h1', content=Text('Oh no, not again!'))
img = Elem('img', attr={'src': 'http://i.imgur.com/pfp3T.jpg'}, tag_type='simple')
body = Elem('body', content=[h1, img])
html = Elem('html', content=[head, body])
print(html)
