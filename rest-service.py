#! /usr/bin/env python
from flask import Flask, jsonify, session, escape
from flask import request
from werkzeug import secure_filename
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

import uuid

import config

app = Flask(__name__)

cfg = config.Config()
connectors = config.init_connectors(cfg)

def make_json_error(ex):
  response = jsonify(message=str(ex))
  response.status_code = (ex.code
                          if isinstance(ex, HTTPException)
                          else 500)
  return response

def output_path(filename):
  return "data/%s" % filename

def response(resp):
  return jsonify(resp)

@app.route("/upload", methods=['POST'])
def upload_file():
    if request.headers['Content-Type'] == 'application/octet-stream':
      fuuid = str(uuid.uuid4())
      f = open(output_path(fuuid), 'wb') 
      f.write(request.data)
      connectors[0].upload(output_path(fuuid))
      return response({'status': 'OK', 'filename': fuuid})
    else:
      return make_json_error({'code':400, 'message':'wrong content-type'})

    #f = request.files['the_file']
    #f.save('/var/www/uploads/' + secure_filename(f.filename))
    #return response(('status', 'OK'))

if __name__ == '__main__':
    for code in default_exceptions.iterkeys():
      app.error_handler_spec[None][code] = make_json_error

    app.run(debug=True)
