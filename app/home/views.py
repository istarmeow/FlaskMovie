from . import home
from flask import render_template, redirect, url_for, flash, session, request
from .forms import RegisterForm, LoginFrom
from app.models import User, UserLog
from werkzeug.security import generate_password_hash
from app import db
import uuid
from functools import wraps


# 要求登录才能访问
def user_login_require(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('login_user', None) is None:
            # 如果session中未找到该键，则用户需要登录
            return redirect(url_for('home.login', next=request.url))
        return func(*args, **kwargs)

    return decorated_function


@home.route("/")
def index():
    return render_template('home/index.html')


@home.route("/indexbanner/")
def indexbanner():
    return render_template('home/indexbanner.html')


@home.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        if not user.check_pwd(data['pwd']):
            flash('密码错误', category='err')
            return redirect(url_for('home.login'))
        session['login_user'] = user.name
        session['login_user_id'] = user.id
        userlog = UserLog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for('home.user'))
    return render_template('home/login.html', form=form)


@home.route('/logout/')
def logout():
    session.pop('login_user', None)
    session.pop('login_user_id', None)
    return redirect(url_for('home.login'))


@home.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            pwd=generate_password_hash(data['pwd']),
            email=data['email'],
            phone=data['phone'],
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash('注册成功', category='ok')
        return redirect(url_for('home.register'))
    return render_template('home/register.html', form=form)


@home.route('/user/')
@user_login_require
def user():
    return render_template('home/user.html')


@home.route('/pwd/')
@user_login_require
def pwd():
    return render_template('home/pwd.html')


@home.route('/comments/')
@user_login_require
def comments():
    return render_template('home/comments.html')


@home.route('/userlog/')
@user_login_require
def userlog():
    return render_template('home/userlog.html')


@home.route('/moviecollect/')
@user_login_require
def moviecollect():
    return render_template('home/moviecollect.html')


@home.route('/search/')
def search():
    return render_template('home/search.html')


@home.route('/play/')
def play():
    return render_template('home/play.html')
