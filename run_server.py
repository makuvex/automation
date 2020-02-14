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
from loadnews import NewsMySql
from pprint import pprint

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

''''''

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

''''''

@app.route('/')
def index():
	#return render_template('test.html', result='')
	service = NewsMySql()
	json = service.loadNews()
	#pprint(json['results'])

	list = []
	# 1. 이미지 썸네일, 2. 헤드라인, 3. 설명, 4. 포스트 날짜 및 출처, 5. detail url
	if(json['status'] == '200'):
		list = json['results']
	return render_template('index_blog_home.html', listhtml=list)

	'''
	{'description': '후베이성 사망자 중복 계산... 전문가 &quot;일관성 있는 기준 필요&quot;',                                                                                                                                             'image': 'http://ojsfile.ohmynews.com/CT_T_IMG/2020/0214/IE002603159_LT.jpg',                                                                                                                                                 'link': 'https://news.google.com/__i/rss/rd/articles/CBMiQ2h0dHA6Ly93d3cub2hteW5ld3MuY29tL05XU19XZWIvVmlldy9hdF9wZy5hc3B4P0NOVE5fQ0Q9QTAwMDI2MTIyMjLSAUFodHRwOi8vbS5vaG15bmV3cy5jb20vTldTX1dlYi9Nb2JpbGUvYW1wLmFzcHg_Q05UTl9DRD1BMDAwMjYxMjIyMg?oc=5',                                                                                                                                                                                                                 'media': None,                                                                                                                                                                                                               'site': '',                                                                                                                                                                                                                   'site_name': '오마이뉴스',                                                                                                                                                                                                     'sno': 65,                                                                                                                                                                                                                   'title': "중국 '코로나19' 사망 121명·확진 5천 명 증가, 통계 '갈팡질팡' - 오마이뉴스",                                                                                                                                                 'type': 'article',                                                                                                                                                                                                           'url': 'http://www.ohmynews.com/NWS_Web/View/at_pg.aspx?CNTN_CD=A0002612222'}]
	'''
	
	
	return render_template('index_blog_home.html', listHtml = ['가','나','다'])	
	#return render_template('index_blog_home.html', listHtml = list)
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