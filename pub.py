import fileinput
import datetime
from flask import *
import os

def contentDump(content, outfile):
	insertContent = False
	for line in fileinput.input(outfile, inplace=1):
	  if line.startswith('<div class="content">'):
	    insertContent = True
	  else:
	    if insertContent:
	      print '<hr /><p>' + content + '<br /><div class="date">' + str(datetime.datetime.now()) + '</div></p>'
	    insertContent = False
	  print line,

def strandize():
	destIP = str(raw_input("User@IP: "))
	destAdd = str(raw_input("Blog Directory(absolute path): "))
	os.system("scp content/index.html content/index.css " + destIP + ":" + destAdd);

def publish(content, preview):
	if preview:
		contentDump(content, 'templates/preview.html')
		return '<a href="%s" target="_blank">Preview</a>' % url_for('show_preview')
	else:
		contentDump(content, 'templates/index.html')
		contentDump(content, 'content/index.html')
		strandize()
		return '<a href="%s" target="_blank">Published</a>' % url_for('show_pubbed')
