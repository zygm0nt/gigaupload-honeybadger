#! /usr/bin/env python
from flask import Flask, jsonify, session, escape
from flask import request, send_file
from werkzeug import secure_filename
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

import uuid
import os

import config
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from os import remove

import urllib3
urllib3.disable_warnings()

app = Flask(__name__)

cfg = config.Config()
connectors = config.init_connectors(cfg)

def make_json_error(ex):
  response = jsonify(message=str(ex))
  response.status_code = (ex.code
                          if isinstance(ex, HTTPException)
                          else 500)
  return response

def response(resp):
  return jsonify(resp)

def temp_file_to_download(filename):
  suffix = filename.split(".")[1]
  tempFileObj = NamedTemporaryFile(mode='w+b',suffix=suffix)
  pilImage = open(filename,'rb')
  copyfileobj(pilImage,tempFileObj)
  pilImage.close()
  remove(filename)
  tempFileObj.seek(0,0)
  return tempFileObj

@app.route("/get/<fuuid>", methods=['GET'])
def download_file(fuuid):
  connectors[0].download("/" + fuuid, "download/%s" % fuuid)
  return send_file(temp_file_to_download('download/%s' % fuuid), as_attachment=True, attachment_filename=fuuid)

@app.route("/upload", methods=['POST'])
def upload_file():
    if request.headers['Content-Type'] == 'application/json':
      fname = request.json['name']
      connectors[0].upload(fname)
      return response({'status': 'OK', 'filename': os.path.basename(fname)})
    else:
      app.logger.error(request.headers['Content-Type'])
      return make_json_error({'code':400, 'message':'wrong content-type'})

if __name__ == '__main__':
    for code in default_exceptions.iterkeys():
      app.error_handler_spec[None][code] = make_json_error

    app.run(debug=True)
