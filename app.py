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
            file1 = upload_file(request.files['file1'])
            file2 = upload_file(request.files['file2'])
            options_list = request.form.getlist('options[]')
            options = " ".join(options_list).replace('-e', '-e temp_uploads'+path_char+'result.xlsx')

            command = "python -m pmix.xlsdiff "+file1+" "+file2+" "+options
            stdout, stderr = _run_background_process(command)
            return render_template('index.html', stderr=stderr, stdout=stdout, export=True)

        except Exception as err:
            msg = 'An unexpected error occurred:\n\n' + str(err)
            return render_template('index.html', stderr=msg)

@app.route('/export', methods=['POST'])
def export():
    upload_folder = basedir + path_char + 'temp_uploads'
    file_path = os.path.join(upload_folder, "result.xlsx")
    return send_file(file_path, None, True, "result.xlsx")

if __name__ == '__main__':
    app.run(debug=True)
