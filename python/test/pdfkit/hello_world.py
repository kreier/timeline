import pdfkit

html_content = """
<html>
  <head>
    <title>Hello, World!</title>
  </head>
  <body>
    <h1>Hello, World!</h1>
  </body>
</html>
"""

pdfkit.from_string(html_content, "hello_world.pdf")

print("PDF created successfully!")
