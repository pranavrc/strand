import fileinput
import datetime
from flask import *
import os
import sys

def contentDump(content, outfile):
	insertContent = False
	delimiter = '<!--Delimiter-->'
	for line in fileinput.input(outfile, inplace=1):
	  if delimiter in line:
	    insertContent = True
	    if insertContent:
	      line = line.replace(delimiter, '<hr /><p>' + content + '<br /><div class="date">' + str(datetime.datetime.now()) + '</div></p>' + delimiter)
	      sys.stdout.write(line)
	    insertContent = False
	    continue
	  print line,

def strandize():
	destIP = str(raw_input("User@IP: "))
	destAdd = str(raw_input("Blog Directory(absolute path): "))
	os.system("scp content/index.html content/index.css " + destIP + ":" + destAdd);

def publish(content, preview):
	if preview:
		indexContent = open('templates/index.html', 'r').read()
		with open('templates/preview.html', 'w') as previewFile:
			previewFile.write(indexContent)
		contentDump(content, 'templates/preview.html')
		previewFile.close()
		return '<a href="%s" target="_blank">Preview</a>' % url_for('show_preview')
	else:
		contentDump(content, 'templates/index.html')
		contentDump(content, 'content/index.html')
		strandize()
		return '<a href="%s" target="_blank">Published</a>' % url_for('show_pubbed')
