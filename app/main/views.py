# -*- coding: utf-8 -*-
import os
import os.path as op
import sys
import time
import datetime
from werkzeug.utils import secure_filename
from . import main
from flask import request, render_template, url_for,\
    send_from_directory, flash, current_app, redirect, session
from ..models import UserData, User
from app import db
from .. import FILE_DIR

# a = current_app.config['UPLOAD_FOLDER']


reload(sys)
sys.setdefaultencoding('utf-8')

print FILE_DIR


# 判断文件后缀
def allowed_file(filename):
    """
    :param filename: 接受文件名
    :return: 返回判断文件是否有 .
    """
    return '.' in filename


def now_time():
    # utc时间
    # now_stamp = time.time()
    # local_time = datetime.datetime.utcfromtimestamp(now_stamp)
    # 本地时间
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return local_time


# 上传db记录
def save_data_db(filename):
    user = session['user']
    print user
    sv_name = filename
    category = 'uploads'

    new_log = UserData(
        username=user, filename=sv_name, category=category, time=now_time())

    db.session.add(new_log)
    db.session.commit()
    db.session.close()


# 下载db记录
def down_data_db(filename):
    user = session['user']
    print user
    sv_name = filename
    category = 'downloads'

    new_log = UserData(
        username=user, filename=sv_name, category=category, time=now_time())

    db.session.add(new_log)
    db.session.commit()
    db.session.close()


@main.route('/')
def upload():
    return render_template('uploads.html', dir_list=FILE_DIR)


# 登陆
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # 判断用户 session 是否存在
        if session.get('user'):
            return '已登陆 %r ' % session['user']
        else:
            return render_template('login.html')
    else:
        name = request.form.get('name', None)
        pwd = request.form.get('password', None)

        user = User.query.filter_by(username=name, password=pwd).first()

        if user:
            # 记录session
            session['user'] = user.username
            print session['user']
            return redirect(url_for('main.upload'))
        else:
            return '账号或密码错误'


# 文件上传
@main.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # 判断用户是否登陆
    if session.get('user'):
        if request.method == 'POST':
            f = request.files['file']
            f_dir = FILE_DIR[0]
            print f_dir
            if not f:
                flash('请选择要上传的文件')
                # return render_template('uploads.html', dir_list=FILE_DIR)
                return redirect(url_for('main.upload'))

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

                        # 记录进数据库
                        save_data_db(filename=filename)

                    f.save(op.join(f_dir, filename))
                    save_data_db(filename=filename)

                    flash("上传成功")
                    return render_template('uploads.html', dir_list=FILE_DIR)

                flash("上传成功")
                return render_template('uploads.html', dir_list=FILE_DIR)
        return 'abc'
    else:
        flash('请登录')
        return render_template('login.html')


@main.route('/manage')
def manage_file():
    size_dic = {}    # 储存文件大小
    file_list = os.listdir(FILE_DIR[0])
    for f in file_list:
        file_size = op.getsize(op.join(FILE_DIR[0], f)) / 1024 / 1024.0
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


@main.route('/download/<filename>')
def download_file(filename):
    if session.get('user'):
        # 判断是文件还是文件夹
        if allowed_file(filename):
            down_data_db(filename=filename)
            return send_from_directory(FILE_DIR[0],
                                       filename,
                                       as_attachment=True)  # as_attachment=True不写即浏览文件

        else:
            new_dir = FILE_DIR[0] + '/' + filename     # 更改dir地址
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
    else:
        flash('请登录')
        return render_template('login.html')

