from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # 创建app对象
app.debug = True  # 开启调试模式
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:3306/movie"  # 定义数据库连接，传入连接，默认端口3306，可不写
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@127.0.0.1:3306/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# 定义db对象，实例化SQLAlchemy，传入app对象
db = SQLAlchemy(app)

if __name__ == '__main__':
    # 先导入所有模型，才能创建数据库
    from app.models import *
    # 创建数据表
    db.create_all()

    # 添加角色
    from app.models import Role
    role = Role(
        name="超级管理员",
        auths="",
    )
    db.session.add(role)
    db.session.commit()

    # 添加管理员
    from werkzeug.security import generate_password_hash
    from app.models import Admin
    admin = Admin(
        name='admin',
        pwd=generate_password_hash('flaskadmin'),  # 加密密码
        is_super=0,
        role_id=1,
    )
    db.session.add(admin)
    db.session.commit()
