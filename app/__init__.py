from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)  # 创建app对象
app.debug = True  # 开启调试模式

# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:3306/movie"  # 定义数据库连接，传入连接，默认端口3306，可不写
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 3306))
if result == 0:
    # 使用本地端口
    use_ip_port = '127.0.0.1:3306'
else:
    # 家里的虚拟机环境连接到宿主机的127.0.0.1
    use_ip_port = '192.168.66.99:3306'
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@{}/movie".format(use_ip_port)

import configparser

config = configparser.ConfigParser()
config.read(r'C:\ProjectConfig.ini')
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db_name}".format(
    user=config['mysql-flaskmovie']['user'],
    password=config['mysql-flaskmovie']['password'],
    host=config['mysql-flaskmovie']['host'],
    port=config['mysql-flaskmovie']['port'],
    db_name=config['mysql-flaskmovie']['db_name']
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = 'b1b7ed6af47d4031acbdeb420658ba84'
# 定义文件上传保存的路径，在__init__.py文件所在目录创建media文件夹，用于保存上传的文件
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/media/')
app.config['USER_IMAGE'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/user/')  # 存放用户头像的路径

# 定义db对象，实例化SQLAlchemy，传入app对象
db = SQLAlchemy(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

# 注册蓝图
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")


# 添加全局404页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
