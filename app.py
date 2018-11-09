"""Web application for XFormTest

http://xform-test.pma2020.org
"""
import platform
import os
import flask
from flask import Flask, render_template, request
# noinspection PyProtectedMember
from static_methods import _run_background_process, upload_file

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
            options_list = request.form.getlist('options[]')
            options = " ".join(options_list)

            command = "python -m pmix.xlsdiff "+base_file+" "+new_file+" "+options
            stdout, stderr = _run_background_process(command)
            return render_template('index.html', stderr=stderr, stdout=stdout)

        except Exception as err:
            msg = 'An unexpected error occurred:\n\n' + str(err)
            return render_template('index.html', stderr=msg)


if __name__ == '__main__':
    app.run(debug=True)
