# coding:utf-8
import os
import sys
import os.path as op
from flask import Flask, request, redirect, url_for, \
    render_template, send_from_directory, flash
from werkzeug.utils import secure_filename

reload(sys)
sys.setdefaultencoding('utf-8')


# 上传地址
UPLOAD_FOLDER = 'C:\Users\wz\Desktop\uploads\static\uploads'
# 限制上传文件类别
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'folder'])

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024

file_dir = app.config['UPLOAD_FOLDER']
# 可以上传文件的dir地址，应该再写个方法，每次重启code时先检查已存在地址,访问调用方法
dir_list = []
dir_list.append(file_dir)


# 判断文件后缀
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def upload():
    return render_template('upload.html', dir_list=dir_list)


# 文件上传
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f_dir = request.form['file_dir']
        print f_dir
        if not f:
            flash('请选择要上传的文件')
            return render_template('upload.html', dir_list=dir_list)
        # 判断上传文件是否符合规范
        if f and allowed_file(f.filename):
            for filenames in request.files.getlist('file'):
                filename = secure_filename(filenames.filename)
                file_path = op.join(f_dir, filename)
                # 判断文件是否存在
                if op.exists(file_path):
                    t1 = filename.split('.')[0]
                    t2 = filename.split('.')[1]
                    t3 = 1
                    t4 = '('
                    t5 = ')'
                    filename = t1 + t4 + str(t3) + t5 + '.' + t2
                    new_file = op.join(f_dir, filename)
                    # 存在同名文件编号递增
                    while op.exists(new_file):
                        t3 += 1
                        # 文件名重写保存
                        filename = t1 + t4 + str(t3) + t5 + '.' + t2
                        new_file = op.join(f_dir, filename)
                    f.save(op.join(f_dir, filename))

                f.save(op.join(f_dir, filename))

            # return redirect(url_for('upload_file',
            #                         filename=filename))
            flash("上传成功")
            return render_template('upload.html', dir_list=dir_list)

        else:
            flash("仅支持txt, pdf, png, jpg, jpeg, gif格式文件上传")
            return render_template('upload.html', dir_list=dir_list)

    return render_template('upload.html', dir_list=dir_list)


@app.route('/manage')
def manage_file():
    size_dic = {}    # 储存文件大小
    file_list = os.listdir(file_dir)
    for f in file_list:
        file_size = op.getsize(op.join(file_dir, f)) / 1024 / 1024.0
        size_dic[f] = file_size
    return render_template('manage.html',
                           file_list=file_list,
                           size_dic=size_dic)


@app.route('/download/<filename>')
def download_file(filename):
    # 判断是文件还是文件夹
    if allowed_file(filename):
        return send_from_directory(file_dir,
                                   filename,
                                   as_attachment=True)  # as_attachment=True不写即浏览文件
    else:
        new_dir = file_dir + '/' + filename     # 更改dir地址
        file_list = os.listdir(new_dir)
        size_dic = {}
        for f in file_list:
            file_size = op.getsize(op.join(new_dir, f)) / 1024 / 1024.0
            size_dic[f] = file_size
        return render_template('manage.html',
                               file_list=file_list,
                               size_dic=size_dic)


@app.route('/test', methods=['GET', 'POST'])
def create():
    f = request.form['filename']
    file_path = op.join(file_dir, f)
    if op.exists(file_path):
        flash("该目录名已存在")
        return render_template('create_folder.html')
    else:
        os.makedirs(file_path)
        flash("创建成功")
        dir_list.append(file_path)
        return render_template('create_folder.html')


@app.route('/create')
def create_folder():
    return render_template("create_folder.html")


# @app.route('/delete/<filename>')
# def delete_file(filename):
#     file_path = op.join(file_dir, filename)
#     os.remove(file_path)
#     return redirect(url_for('manage_file'))


# @app.route('/search')
# def search_file():
#     file_list = os.listdir(file_dir)
#     return render_template('search.html', file_list=file_list)


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
