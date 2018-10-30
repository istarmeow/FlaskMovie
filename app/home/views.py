from . import home
from flask import render_template, redirect, url_for, flash, session, request
from .forms import RegisterForm, LoginFrom, UserDetailForm, PwdForm, CommentForm
from app.models import User, UserLog, Preview, Movie, MovieCollect, Comment, Tag
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
from app import db, app
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


@home.route("/<int:page>/")
def index(page):
    if not page:
        page = 1
    all_tag = Tag.query.all()
    # 星级转换
    star_list = [(1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')]
    all_star = map(lambda x: {'num': x[0], 'info': x[1]}, star_list)
    # 年份列表
    import time
    now_year = time.localtime()[0]
    year_range = [year for year in range(int(now_year)-1, int(now_year)-5, -1)]
    # print(year_range)
    page_movies = Movie.query
    selected = dict()
    tag_id = request.args.get('tag_id', 0)  # 获取链接中的标签id，0为显示所有
    if int(tag_id) != 0:
        page_movies = page_movies.filter_by(tag_id=tag_id)
    selected['tag_id'] = tag_id

    star_num = request.args.get('star_num', 0)  # 获取星级数字，0为显示所有
    if int(star_num) != 0:
        page_movies = page_movies.filter_by(star=star_num)
    selected['star_num'] = int(star_num)

    time_year = request.args.get('time_year', 1)  # 1为所有日期，0为更早，月份为所选
    from sqlalchemy import extract, exists, between
    if int(time_year) == 0:
        page_movies = page_movies  # !!!没写这个功能
    elif int(time_year) == 1:
        page_movies = page_movies  # 所有年份的电影
    else:
        page_movies = page_movies.filter(extract('year', Movie.release_time) == time_year)  # 筛选年份
    selected['time_year'] = time_year

    play_num = request.args.get('play_num', 1)  # 1为从高到低，0为从低到好
    if int(play_num) == 1:
        page_movies = page_movies.order_by(
            Movie.play_num.desc()
        )
    else:
        page_movies = page_movies.order_by(Movie.play_num.asc())
    selected['play_num'] = play_num

    comment_num = request.args.get('comment_num', 1)  # 1为从高到低，0为从低到好
    if int(comment_num) == 1:
        page_movies = page_movies.order_by(
            Movie.comment_num.desc()
        )
    else:
        page_movies = page_movies.order_by(Movie.comment_num.asc())
    selected['comment_num'] = comment_num

    page_movies = page_movies.paginate(page=page, per_page=12)
    return render_template('home/index.html',
                           all_tag=all_tag,
                           all_star=all_star,
                           now_year=now_year,
                           year_range=year_range,
                           selected=selected,
                           page_movies=page_movies)


@home.route("/indexbanner/")
def indexbanner():
    previews = Preview.query.all()
    return render_template('home/indexbanner.html', previews=previews)


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


@home.route('/user/', methods=['GET', 'POST'])
@user_login_require
def user():
    login_user = User.query.get_or_404(int(session['login_user_id']))
    form = UserDetailForm(
        name=login_user.name,
        email=login_user.email,
        phone=login_user.phone,
        info=login_user.info
    )
    form.face.validators = []
    form.face.render_kw = {'required': False}
    if form.validate_on_submit():
        data = form.data
        face_save_path = app.config['USER_IMAGE']
        if not os.path.exists(face_save_path):
            os.makedirs(face_save_path)  # 如果文件保存路径不存在，则创建一个多级目录
            import stat
            os.chmod(face_save_path, stat.S_IRWXU)  # 授予可读写权限

        if form.face.data:
            # 上传文件不为空保存
            if login_user.face and os.path.exists(os.path.join(face_save_path, login_user.face)):
                os.remove(os.path.join(face_save_path, login_user.face))
            # 获取上传文件名称
            file_face = secure_filename(form.face.data.filename)
            # !!!AttributeError: 'str' object has no attribute 'filename'，前端需要加上enctype="multipart/form-data"
            from app.admin.views import change_filename
            login_user.face = change_filename(file_face)
            form.face.data.save(face_save_path + login_user.face)

        if login_user.name != data['name'] and User.query.filter_by(name=data['name']).count() == 1:
            flash('昵称已经存在', 'err')
            return redirect(url_for('home.user'))
        login_user.name = data['name']

        if login_user.email != data['email'] and User.query.filter_by(email=data['email']).count() == 1:
            flash('邮箱已经存在', 'err')
            return redirect(url_for('home.user'))
        login_user.email = data['email']

        if login_user.phone != data['phone'] and User.query.filter_by(phone=data['phone']).count() == 1:
            flash('手机号已经存在', 'err')
            return redirect(url_for('home.user'))
        login_user.phone = data['phone']

        login_user.info = data['info']

        db.session.commit()
        flash('修改资料成功', 'ok')
        return redirect(url_for('home.user'))
    return render_template('home/user.html', form=form, login_user=login_user)


@home.route('/pwd/', methods=['GET', 'POST'])
@user_login_require
def pwd():
    login_user = User.query.get_or_404(int(session['login_user_id']))
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        if login_user.check_pwd(data['oldpwd']):
            login_user.pwd = generate_password_hash(data['newpwd'])
            db.session.commit()
            flash('密码修改成功，请重新登录', category='ok')
            return redirect(url_for('home.login'))
        else:
            flash('旧密码不正确', category='err')
            return redirect(url_for('home.pwd'))
    return render_template('home/pwd.html', form=form)


@home.route('/comments/<int:page>/')
@user_login_require
def comments(page):
    if not page:
        page = 1
    page_comments =Comment.query.filter_by(
        user_id=int(session['login_user_id'])
    ).order_by(
        Comment.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/comments.html', page_comments=page_comments)


@home.route('/userlog/<int:page>/')
@user_login_require
def userlog(page=None):
    """会员登录日志"""
    if not page:
        page = 1
    page_user_logs = UserLog.query.filter_by(
        user_id=int(session['login_user_id'])
    ).order_by(
        UserLog.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/userlog.html', page_user_logs=page_user_logs)


@home.route('/moviecollect/<int:page>/')
@user_login_require
def moviecollect(page):
    if not page:
        page = 1
    page_moviecollects = MovieCollect.query.filter_by(
        user_id=int(session['login_user_id'])
    ).order_by(
        MovieCollect.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/moviecollect.html', page_moviecollects=page_moviecollects)


@home.route('/search/')
def search():
    keyword = request.args.get('keyword')
    search_movies = Movie.query.filter(
        Movie.title.ilike("%" + keyword + "%")
    ).order_by(
        Movie.add_time.desc()
    )
    search_count = Movie.query.filter(Movie.title.ilike("%" + keyword + "%")).count()
    return render_template('home/search.html', keyword=keyword, search_movies=search_movies, search_count=search_count)


@home.route('/play/<int:movie_id>/page/<int:page>/', methods=['GET', 'POST'])
def play(movie_id=None, page=None):
    movie = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id,
        Movie.id == int(movie_id)
    ).first_or_404()

    if request.method == 'GET' and int(request.args.get('page', 0)) != 1:
        movie.play_num += 1  # 访问量加1
        db.session.commit()

    form = CommentForm()
    if 'login_user' not in session:
        form.submit.render_kw = {
            'disabled': "disabled",
            "class": "btn btn-success",
            "id": "btn-sub"
        }
    if form.validate_on_submit() and 'login_user' in session:
        data = form.data
        comment = Comment(
            content=data['content'],
            movie_id=movie.id,
            user_id=session['login_user_id']
        )
        db.session.add(comment)
        movie.comment_num += 1
        db.session.commit()
        flash('评论成功', category='ok')
        return redirect(url_for('home.play', movie_id=movie.id, page=1))

    if page is None:
        page = 1
    # 查询的时候关联标签，采用join来加进去,多表关联用filter,过滤用filter_by
    page_comments = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == movie.id,
        User.id == Comment.user_id
    ).order_by(
        Comment.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/play.html', movie=movie, form=form, page_comments=page_comments)


@home.route('/moviecollect/add/')
@user_login_require
def add_moviecollect():
    movie_id = request.args.get('movie_id', '')
    user_id = request.args.get('user_id', '')
    movie_collect = MovieCollect.query.filter_by(
        user_id=int(user_id),
        movie_id=int(movie_id)
    )
    if movie_collect.count() == 1:
        data = dict(ok=0)
    if movie_collect.count() == 0:
        movie_collect = MovieCollect(
            user_id=int(user_id),
            movie_id=int(movie_id)
        )
        db.session.add(movie_collect)
        db.session.commit()
        data = dict(ok=1)
    import json
    return json.dumps(data)