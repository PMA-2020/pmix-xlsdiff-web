"""Web application for XFormTest

http://xform-test.pma2020.org
"""
import platform
import os
import flask
from flask import Flask, render_template, request, send_file
# noinspection PyProtectedMember
from static_methods import _run_background_process, upload_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
path_char = '\\' if platform.system() == 'Windows' else '/'


@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        return render_template('index.html')
    else:
        try:
            base_file = upload_file(request.files['base-file'])
            new_file = upload_file(request.files['new-file'])
            new_file_name = secure_filename(request.files['new-file'].filename)
            options_list = request.form.getlist('options[]')
            options = " ".join(options_list)

            command = "python -m pmix.xlsdiff "+base_file+" "+new_file+" "+options
            stdout, stderr = _run_background_process(command)
            return render_template('index.html', stderr=stderr, stdout=stdout, new_file_path=new_file, new_file_name=new_file_name)

        except Exception as err:
            msg = 'An unexpected error occurred:\n\n' + str(err)
            return render_template('index.html', stderr=msg)

@app.route('/export', methods=['POST'])
def export():
    new_file_path = request.form['new_file_path']
    new_file_name = request.form['new_file_name']
    return send_file(new_file_path, None, True, new_file_name)

if __name__ == '__main__':
    app.run(debug=True)
