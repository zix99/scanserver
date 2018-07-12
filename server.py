#!/usr/bin/env python
from bottle import route, run, template, post, response, request
import subprocess
import time

PORT = 9012

@route('/')
def scanpage():
	return template('scan')

@post('/scan')
def scan():
	ppi = int(request.forms.get('ppi'))
	mode = request.forms.get('mode')

	cmd = "scanimage --format=tiff --resolution %d --mode %s" % (ppi, mode)
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, close_fds=True)

	response.add_header('Content-type', 'image/gif')

	while True:
		buf = p.stdout.read(1024)
		if not buf: break
		yield buf

run(host='0.0.0.0', port=PORT, debug=True)