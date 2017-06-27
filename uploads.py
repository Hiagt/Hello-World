# coding:utf-8
import os
import os.path as op
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import multiprocessing
import urllib

# 上传地址
UPLOAD_FOLDER = 'F:\uploads\static\uploads'
# 限制上传文件类别
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024

file_dir = app.config['UPLOAD_FOLDER']


# 判断文件后缀
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def upload():
    return render_template('upload.html')


# 文件上传
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # 判断上传文件是否符合规范
        if f and allowed_file(f.filename):
            for filenames in request.files.getlist('file'):
                filename = secure_filename(filenames.filename)
                file_path = op.join(file_dir, filename)
                # 判断文件是否存在
                if op.exists(file_path):
                    t1 = filename.split('.')[0]
                    t2 = filename.split('.')[1]
                    t3 = 1
                    t4 = '('
                    t5 = ')'
                    filename = t1 + t4 + str(t3) + t5 + '.' + t2
                    new_file = op.join(file_dir, filename)
                    # 存在同名文件编号递增
                    while op.exists(new_file):
                        t3 += t3
                        # 文件名重写保存
                        filename = t1 + t4 + str(t3) + t5 + '.' + t2
                        new_file = op.join(file_dir, filename)
                    f.save(os.path.join(file_dir, filename))

                f.save(os.path.join(file_dir, filename))

            return redirect(url_for('upload_file',
                                    filename=filename))

    return render_template('upload.html')


@app.route('/manage')
def manage_file():
    file_list = os.listdir(file_dir)
    return render_template('manage.html', file_list=file_list)


@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = op.join(file_dir, filename)
    os.remove(file_path)
    return redirect(url_for('manage_file'))


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(file_dir, filename, as_attachment=True)


@app.route('/search')
def search_file():
    file_list = os.listdir(file_dir)
    return render_template('search.html', file_list=file_list)


# @app.route('/search/download', methods=['GET', 'POST'])
# def search_download():
#     file_name = request.values.getlist('files')
#     print file_name
#     for f in file_name:
#     #     return send_from_directory(file_dir, f, as_attachment=True)
#         while True:
#             try:
#                 urllib.urlretrieve(file_dir, f)
#             except Exception, e:
#                 print e
#             else:
#                 break


if __name__ == '__main__':
    app.run(debug=True)
