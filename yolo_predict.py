#! /usr/bin/env python3
import subprocess
import subprocess
import os
import re
import base64
from flask import Flask, request, jsonify, Response
from requests_toolbelt import MultipartEncoder

def YOLO(filename: str):
	print(filename)
	result = subprocess.check_output('./darknet detector test obj.data yolov3-obj.cfg yolov3-obj_final.weights static/images/'+filename, shell=True)
	os.system('mv predictions.jpg ./static/images/')
	result = str(result)
	p = re.compile("[Ab]*Normal ToothBrush: ...")
	result = p.findall(result)
	
	return result[0]

app = Flask(__name__)
@app.route('/tooth/image_process', methods = ['POST'])
def imageProcessing():

	f = request.files['file']
	
	f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename)) # 해당 파일 저장
	result = YOLO(f.filename)
	with open('static/images/predictions.jpg', 'rb') as img:
		upload = base64.b64encode(img.read()).decode('utf8')

		data = { 
			"result" : result,
			"img" :  upload
		}	
		return data

if __name__ == "__main__":
	app.config['UPLOAD_FOLDER'] = 'static/images'	
	app.run(host='0.0.0.0', port=20002)


