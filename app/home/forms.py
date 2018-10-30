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


class UserDetailForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[
            DataRequired('请输入昵称！')
        ],
        description='昵称',
        render_kw={
            'class': "form-control",
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
            'class': "form-control",
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
            'class': "form-control",
            'placeholder': "请输入手机",
            'required': "required",
            'autofocus': "autofocus"
        }
    )
    face = FileField(
        label='头像',
        validators=[
            DataRequired('请上传头像')
        ],
        description='头像',
    )
    info = TextAreaField(
        label='简介',
        validators=[
            DataRequired('请输入简介！')
        ],
        description='简介',
        render_kw={
            'class': "form-control",
            'rows': "10",
        }
    )
    submit = SubmitField(
        label='保存',
        render_kw={
            'class': "btn btn-success"
        }
    )


class PwdForm(FlaskForm):
    oldpwd = PasswordField(
        label='旧密码',
        validators=[
            DataRequired('请输入旧密码！')
        ],
        description='旧密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入旧密码",
            'required': "required",
            'autofocus': 'autofocus'
        }
    )
    newpwd = PasswordField(
        label='新密码',
        validators=[
            DataRequired('请输入新密码！')
        ],
        description='新密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入新密码",
            'required': "required",
            'autofocus': 'autofocus'
        }
    )
    repwd = PasswordField(
        label='重复密码',
        validators=[
            DataRequired('请输入重复密码！'),
            EqualTo('newpwd', message='两次密码不一致')
        ],
        description='重复密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入重复密码",
            'required': "required"
        }
    )
    submit = SubmitField(
        label='修改密码',
        render_kw={
            'class': "btn btn-success"
        }
    )


class CommentForm(FlaskForm):
    content = TextAreaField(
        label='内容',
        validators=[
            DataRequired('请输入内容')
        ],
        description='内容',
        render_kw={
            # 'id': "input_content"
            'class': "form-control",
            'rows': "5"
        }
    )
    submit = SubmitField(
        label='提交评论',
        render_kw={
            "class": "btn btn-success",
            "id": "btn-sub"
        }
    )
