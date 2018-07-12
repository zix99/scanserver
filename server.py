#!/usr/bin/env python
from bottle import route, run, template, post, response, request, redirect, abort, static_file
from PIL import Image
from StringIO import StringIO
import subprocess
import time
import os

PORT = 9012
SCAN_DIR = 'scans/'

if not os.path.isdir(SCAN_DIR):
	os.mkdir(SCAN_DIR)

page = 1

@route('/')
def scanpage():
	files = os.listdir(SCAN_DIR)
	file_details = []
	for f in files:
		if f.endswith("jpg"):
			stat = os.stat(SCAN_DIR + f)
			file_details.append({
				"name": f,
				"size": stat.st_size,
				"ts": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime)),
				})

	return template('scan', files=file_details)

@route('/scans/<filename>')
def convert(filename):
	return static_file(filename, root=SCAN_DIR)

@post('/scan')
def scan():
	global page
	ppi = int(request.forms.get('ppi'))
	mode = request.forms.get('mode')

	cmd = "scanimage --format=tiff --resolution %d --mode %s" % (ppi, mode)
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, close_fds=True)

	stream = StringIO()
	while True:
		buf = p.stdout.read(1024)
		if not buf: break
		stream.write(buf)

	img = Image.open(stream)
	img.save(SCAN_DIR + 'page-%d.jpg' % page, 'JPEG', quality=95)
	page += 1

	redirect('/?xnav=scan')

@route('/pdf')
def pdf():
	files = map(lambda x: SCAN_DIR + x, sorted(os.listdir(SCAN_DIR)))
	cmd = "convert %s +compress pdf:-" % (str.join(' ', files))
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, close_fds=True)

	response.add_header('Content-type', 'application/pdf')

	while True:
		buf = p.stdout.read(1024)
		if not buf: break
		yield buf

@route('/scans/<filename>/delete')
def delete(filename):
	os.unlink(SCAN_DIR + filename)
	redirect('/?xnav=deletefile')

@route('/deleteall')
def delete():
	for f in os.listdir(SCAN_DIR):
		os.unlink(SCAN_DIR + f)

	redirect('/?xnav=delete')

run(host='0.0.0.0', port=PORT, debug=True)
