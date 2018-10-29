from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FileField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Regexp

from app.models import User


class RegisterForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[
            DataRequired('请输入昵称！')
        ],
        description='昵称',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入昵称",
            'required': "required",
            'autofocus': "autofocus"
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('请输入邮箱！'),
            Email('邮箱格式不正确')
        ],
        description='邮箱',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入邮箱",
            'required': "required",
            'autofocus': "autofocus"
        }
    )
    phone = StringField(
        label='手机',
        validators=[
            DataRequired('请输入手机！'),
            Regexp('^1[3|4|5|6|7|8][0-9]\d{4,8}$', message='手机格式不正确')
        ],
        description='手机',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入手机",
            'required': "required",
            'autofocus': "autofocus"
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码！')
        ],
        description='密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入密码",
            'required': "required"
        }
    )
    repwd = PasswordField(
        label='重复密码',
        validators=[
            DataRequired('请输入重复密码！'),
            EqualTo('pwd', message='两次密码不一致')
        ],
        description='重复密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入重复密码",
            'required': "required"
        }
    )
    submit = SubmitField(
        label='注册',
        render_kw={
            'class': "btn btn-lg btn-success btn-block"
        }
    )

    def validate_name(self, field):
        name = field.data
        num = User.query.filter_by(name=name).count()
        if num == 1:
            raise ValidationError('昵称已经存在，请重新输入')

    def validate_email(self, field):
        email = field.data
        num = User.query.filter_by(email=email).count()
        if num == 1:
            raise ValidationError('邮箱已经存在，请重新输入')

    def validate_phone(self, field):
        phone = field.data
        num = User.query.filter_by(phone=phone).count()
        if num == 1:
            raise ValidationError('手机号已经存在，请重新输入')


class LoginFrom(FlaskForm):
    """会员登录表单"""
    name = StringField(
        label='账号',
        validators=[
            DataRequired('请输入账号！')
        ],
        description='账号',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入账号",
            'required': "required"
        }
    )

    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入密码！')
        ],
        description='密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入密码",
            'required': "required",
            'autofocus': 'autofocus'
        }
    )
    submit = SubmitField(
        label='登录',
        render_kw={
            'class': "btn btn-lg btn-success btn-block"
        }
    )

    def validate_name(self, field):
        """从Admin数据库中，检测账号是否存在，如果不存在则在account.errors中添加错误信息"""
        account = field.data
        num = User.query.filter_by(name=account).count()
        if num == 0:
            raise ValidationError('账号不存在')
