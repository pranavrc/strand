import fileinput

def publish(content):
	insertContent = False

	for line in fileinput.input('content/index.html', inplace=1):
	  if line.startswith('<div class="content">'):
	    insertContent = True
	  else:
	    if insertContent:
	      print '<p>' + content + '</p>'
	    insertContent = False
	  print line,

