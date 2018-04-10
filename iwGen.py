# -*- coding: utf-8 -*-
import os
import shutil
import json
from PIL import Image
from bottle import route, run, template, static_file
from gevent import monkey

import azLib as al

DIR_THUMB = 'thumb'
currentFileLst = ''

def imgCompress(fname, sname):
	img = Image.open(fname)
	img.thumbnail((128, 128))
	img.save(sname, 'PNG')

def fileStructure():
	
	fo = al.FileOperation()
	fileLst = fo.fileLstMaker('.', ['.jpg', '.jpeg', '.gif', '.png', '.JPG', '.PNG'])
	classified = {}

	currentFolder = ''
	for p in fileLst:
		tmp = os.path.split(p)
		# print tmp
		fname = tmp[-1]
		folder = tmp[0]
		imgCompress(p, './%s/'%DIR_THUMB + fname)
		if folder == currentFolder:
			classified[folder.replace('\\', '/')].append([p.replace('\\', '/'), fname])
		else:
			classified[folder.replace('\\', '/')] = [[p.replace('\\', '/'), fname]]
		currentFolder = folder
	return classified


def fileLst2JSON():
	return json.dumps(fileStructure())


@route('/')
def access():
	global currentFileLst
	currentFileLst = fileLst2JSON()
	with open('index.htm', 'r') as o:
		return o.read().replace('{{file_json}}', currentFileLst).encode('utf-8')

@route('/viewer.htm')
def viewer():
	with open('viewer.htm', 'r') as o:
		return o.read().replace('{{dict_files}}', currentFileLst+'[cata]').encode('utf-8')

@route('/thumb/<imgName>')
def thumbViewer(imgName):
	return static_file(imgName, root='./thumb')

@route('/<cata>/<imgName>')
def imgViewer(cata, imgName):
	return static_file(imgName, root='./'+cata)

@route('/<fname>')
def default(fname):
	# name, ext = os.path.splitext(fname)
	# if ext not in ['.jpg', '.JPG', '.png', '.PNG', '.jpeg', '.gif', '.GIF']:
	with open(fname, 'r') as o:
		return o.read()


if __name__ == '__main__':
	monkey.patch_all()
	run(host='0.0.0.0', port=8005, debug=True, server='gevent')
