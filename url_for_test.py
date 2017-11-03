from flask import Flask, request, render_template, session, url_for, redirect
# from shopping_trolley.admain_db import db, User
# from shopping_trolley.commodity_db import db, Commodity


app = Flask(__name__)


@app.route('/shop')
def shop_form():
    return render_template("shopping.html")


@app.route('/login')
def login_form():
    return render_template("login.html")


@app.route('/login', methods=['GET', ' POST'])
def login():
    name = request.form.get('name', None)
    pwd = request.form.get('password', None)

    if name == '1' and pwd == '2':
        return redirect(url_for('shop'))
        # return render_template('shopping.html')
    else:
        return '123'


if __name__ == '__main__':
    app.run()
