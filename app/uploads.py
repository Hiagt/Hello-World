# coding:utf-8
import os
import os.path as op
import sys
import urllib2, urllib
from flask import Flask, request, redirect, url_for, \
    render_template, send_from_directory, flash
from werkzeug.utils import secure_filename
from config import config

reload(sys)
sys.setdefaultencoding('utf-8')


app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')      # 直接调用方法或用config字典
# or app.config.from_object(config['development'])

# app.config.from_pyfile('config.py')

file_dir = app.config['UPLOAD_FOLDER']
down_dir = app.config['DOWNLOAD_FOLDER']


# 可以上传文件的dir地址，应该再写个方法，每次重启code时先检查已存在地址,访问调用方法
dir_list = []
dir_list.append(file_dir)


# 判断文件后缀
def allowed_file(filename):
    return '.' in filename


# 下载文件
def save_file(url, file_name, file_path=down_dir):
    try:
        if not op.exists(file_path):
            os.makedirs(file_path)
        f_name = op.join(file_path, file_name)
        urllib.urlretrieve(url, f_name)
    except IOError as e:
        print 'error', e
    except Exception as e:
        print 'error', e


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

            flash("上传成功")
            return render_template('upload.html', dir_list=dir_list)
    return render_template('upload.html', dir_list=dir_list)


@app.route('/manage')
def manage_file():
    size_dic = {}    # 储存文件大小
    file_list = os.listdir(file_dir)
    for f in file_list:
        file_size = op.getsize(op.join(file_dir, f)) / 1024 / 1024.0
        size_dic[f] = file_size

    # 根据文件名进行排序
    for num in range(len(file_list) - 1, 0, -1):
        for i in range(num):
            o1 = file_list[i].split('.')[0]
            t1 = file_list[i + 1].split('.')[0]

            if o1 > t1:
                temp = file_list[i]
                file_list[i] = file_list[i + 1]
                file_list[i + 1] = temp

    return render_template('manage.html',
                           file_list=file_list,
                           size_dic=size_dic)


@app.route('/download/<filename>')
def download_file(filename):
    # 判断是文件还是文件夹
    if allowed_file(filename):
        # return send_from_directory(file_dir,
        #                            filename,
        #                            as_attachment=True)  # as_attachment=True不写即浏览文件
        # d_dir = op.join(down_dir, filename)
        url = 'http://127.0.0.1:5000/download' + '/' + filename

        r = request.get(url, verify=False)
        print r.content
        with open(down_dir, "wb") as code:
            code.write(r.content)

        # save_file(url, file_name=filename)
        # return redirect(url_for(manage_file))
    else:
        new_dir = file_dir + '/' + filename     # 更改dir地址
        file_list = os.listdir(new_dir)
        size_dic = {}
        for f in file_list:
            file_size = op.getsize(op.join(new_dir, f)) / 1024 / 1024.0
            size_dic[f] = file_size

        # 根据文件名进行排序
        for num in range(len(file_list)-1, 0, -1):
            for i in range(num):
                o1 = file_list[i].split('.')[0]
                t1 = file_list[i+1].split('.')[0]
                if o1 > t1:
                    temp = file_list[i]
                    file_list[i] = file_list[i+1]
                    file_list[i+1] = temp

        return render_template('manage.html',
                               file_list=file_list,
                               size_dic=size_dic)


if __name__ == '__main__':
    app.run()
