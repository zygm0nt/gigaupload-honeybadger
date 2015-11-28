#! /usr/bin/env python
from flask import Flask, jsonify, session, escape
from flask import request
from werkzeug import secure_filename
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

import uuid


app = Flask(__name__)


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

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route("/upload", methods=['POST'])
def upload_file():
    if request.headers['Content-Type'] == 'application/octet-stream':
      uuid = str(uuid.uuid4())
      f = open(output_path(uuid), 'wb') 
      f.write(request.data)
      return response({'status': 'OK', 'filename': uuid})
    else:
      return make_json_error({'code':400, 'message':'wrong content-type'})

    #f = request.files['the_file']
    #f.save('/var/www/uploads/' + secure_filename(f.filename))
    #return response(('status', 'OK'))

if __name__ == '__main__':
    for code in default_exceptions.iterkeys():
      app.error_handler_spec[None][code] = make_json_error

    app.run(debug=True)
