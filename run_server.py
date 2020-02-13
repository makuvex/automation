# -*- coding: utf-8 -*-
 
from flask import Flask, request, render_template
from flask import redirect, url_for, flash, send_file, Response, jsonify, Blueprint
from werkzeug.utils import secure_filename
import pandas
from tabula import read_pdf
import camelot
from io import StringIO
import codecs
import json

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(file):
    return '.' in file and \
           file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
def get_ip():
	return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
	
def make_filename(file):
	ip = f'{get_ip()}'
	name = file.filename.rsplit('.',1)[0]
	return ip + '_' + name + '.xlsx'
	
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.secret_key = b'bootstrap'

@app.route('/insert', methods=['GET'])
def insert():
	print('@@@ call insert')

	return render_template('test.html',
                           result='insert is done!',
                           resultData=None,
                           resultUPDATE=None)

@app.route('/_add_numbers')
def add_numbers():
	print('@@@ call _add_numbers')
	a = request.args.get('a', 0, type=int)
	b = request.args.get('b', 0, type=int)
	file = open('templates/index_form.html', 'r', encoding='utf-8')
	return jsonify(result=file.read())
	#return jsonify(result='<html><head><title>AJAX Loaded Title</title></head><body>It works!</body></html>')

@app.route('/')
def index():
	#return render_template('test.html', result='')
	return render_template('index_blog_home.html')
	#return render_template('index_form.html')

@app.route('/uploads/<error>')
def render_file(error):
	return render_template('error.html', errorhtml=error)

@app.route('/xlsx_file_download_with_file')
def xlsx_file_download(file):
	filename = f'uploads/{make_filename(file)}'
	print('@@@ download filename %s'%filename)
	return send_file(filename,
					mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
					attachment_filename=f'{make_filename(file)}',
					as_attachment=True)
	
	
@app.route('/file_uploaded', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file_upload']
		print('@@@ file %s'%{file})
		print('@@@ filename %s'%{file.filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS})
		
		if file and allowed_file(file.filename):
			#print('allowed file')
			file.save(f'uploads/{secure_filename(file.filename)}')
			tables = camelot.read_pdf(f'uploads/{secure_filename(file.filename)}', pages = "all", multiple_tables = False)
			tables.export(f'uploads/{make_filename(file)}', f = "excel")
			return xlsx_file_download(file)
			#return redirect(url_for('index'))
		print('not allowed file')
		#return redirect(url_for('render_file', error='pdf가 아님'))
	flash('잘못된 파일을 선택 했네요')		
	return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)


#출처: https://qkqhxla1.tistory.com/901 [archives]