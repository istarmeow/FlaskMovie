from . import home
from flask import render_template, redirect, url_for


@home.route("/")
def index():
    return render_template('home/index.html')


@home.route("/indexbanner/")
def indexbanner():
    return render_template('home/indexbanner.html')


@home.route('/login/')
def login():
    return render_template('home/login.html')


@home.route('/logout/')
def logout():
    return redirect(url_for('home.login'))


@home.route('/register/')
def register():
    return render_template('home/register.html')


@home.route('/user/')
def user():
    return render_template('home/user.html')


@home.route('/pwd/')
def pwd():
    return render_template('home/pwd.html')


@home.route('/comments/')
def comments():
    return render_template('home/comments.html')


@home.route('/userlog/')
def userlog():
    return render_template('home/userlog.html')


@home.route('/moviecollect/')
def moviecollect():
    return render_template('home/moviecollect.html')


@home.route('/search/')
def search():
    return render_template('home/search.html')


@home.route('/play/')
def play():
    return render_template('home/play.html')