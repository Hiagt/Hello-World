#  登陆
#  商品展示页面
#  选择商品，加入购物车
#  判断是否登陆,True加入购物车 False给出结果未登陆
#  购物车页面
#  增减商品数量


from flask import Flask, request, render_template, session, url_for
from shopping_trolley.admain_db import db, User
# from shopping_trolley.commodity_db import db, Commodity


app = Flask(__name__)
app.secret_key = 'it is secret key'
app.config['SESSION_TYPE'] = 'filesystem'

current_user = None


# 注册
@app.route('/signup')
def signup_form():
    return render_template('signup.html')


# 商品页面
@app.route('/shop')
def shop_form():
    return render_template("shopping.html")


# 购物车
@app.route('/shop_trolley')
def shop_trolley_form():
    return render_template('shopping_trolley.html')

# with app.test_request_context():
    # print(url_for('shop_form'))


# 登陆
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form.get('name', None)
        pwd = request.form.get('password', None)

        user = User.query.filter_by(username=name, password=pwd).first()

        if user:
            # session['current_user'] = user
            return url_for('shop_form')
        else:
            return '账号或密码错误'


# 注册
@app.route('/signup', methods=['POST'])
def signup():
    signup_name = request.form.get('signup_name', None)
    signup_pwd = request.form.get('signup_pwd', None)
    signup_email = request.form.get('signup_email', None)

    if not signup_name or not signup_pwd or not signup_email:
        return '请输入账号密码'

    add_user = User(signup_name, signup_pwd, signup_email)

    db.session.add(add_user)
    db.session.commit()

    if add_user.id:
        return '注册成功'
    else:
        return '注册失败'


if __name__ == '__main__':
    app.run()
