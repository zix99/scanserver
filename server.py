#!/usr/bin/env python
from bottle import route, run, template, post, get, response, request, redirect, abort, static_file
from PIL import Image
from StringIO import StringIO
import subprocess
import time
import os

PORT = 9012
SCAN_DIR = 'scans/'
TEST_IMAGE = os.getenv('TEST_IMAGE')

if not os.path.isdir(SCAN_DIR):
	os.mkdir(SCAN_DIR)

def buildScanFileArray():
	files = os.listdir(SCAN_DIR)
	file_details = []
	for f in sorted(files):
		if f.endswith("jpg"):
			stat = os.stat(SCAN_DIR + f)
			file_details.append({
				"name": f,
				"size": stat.st_size,
				"ts": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime)),
				})
	return file_details

@route('/')
def scanpage():
	return template('scan', files=buildScanFileArray())

@route('/scans/<filename>')
def convert(filename):
	return static_file(filename, root=SCAN_DIR)

@get('/scan')
def scanredir():
	redirect('/')

@post('/scan')
def scan():
	ppi = int(request.forms.get('ppi'))
	mode = request.forms.get('mode')
	autocrop = request.forms.get('autocrop', False)

	if TEST_IMAGE:
		stream = TEST_IMAGE
	else:
		cmd = "scanimage --format=tiff --resolution %d --mode %s" % (ppi, mode)
		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

		stream = StringIO()
		while True:
			buf = p.stdout.read(1024)
			if not buf: break
			stream.write(buf)

		retcode = p.wait()
		reterr = p.stderr.read()
		print reterr

		if retcode != 0:
			return template('scan', files=buildScanFileArray(), err='Scanimage returned code %d.  Is the printer on?\n%s' % (retcode, reterr))

	img = Image.open(stream)
	filename = 'page-%d.jpg' % time.time()
	img.save(SCAN_DIR + filename, 'JPEG', quality=95)

	if autocrop:
		# Experimental feature.. doesn't seem to work great atm
		area = subprocess.Popen("convert %s -morphology Dilate:5 Diamond:5,3 -fuzz 10%% -trim -format '%%xx%%h%%O' info:-" % (SCAN_DIR + filename), shell=True, stdout=subprocess.PIPE).stdout.read()
		print area
		cropProc = subprocess.Popen('convert %s -crop %s %s' % (SCAN_DIR + filename, area, SCAN_DIR + filename + '.other'), shell=True)
		if cropProc.wait() != 0:
			return template('scan', files=buildScanFileArray(), err='Scan autocrop returned code.')



	return template('scan', files=buildScanFileArray(), image=filename)

@route('/pdf')
def pdf():
	files = map(lambda x: SCAN_DIR + x, sorted(os.listdir(SCAN_DIR)))
	cmd = "convert %s -compress jpeg pdf:-" % (str.join(' ', files))
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

run(host='0.0.0.0', port=PORT, debug=True, reloader=True if TEST_IMAGE else False)
