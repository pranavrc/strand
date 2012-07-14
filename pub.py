import fileinput
import datetime

def contentDump(content):
	insertContent = False
	for line in fileinput.input('content/index.html', inplace=1):
	  if line.startswith('<div class="content">'):
	    insertContent = True
	  else:
	    if insertContent:
	      print '<hr /><p>' + content + '<br />' + str(datetime.datetime.now()) + '</p>'
	    insertContent = False
	  print line,

def publish(content):
	contentDump(content)
	return 'Published'
