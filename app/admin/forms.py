from flask_wtf import FlaskForm  # 表单基类
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FileField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Admin, Tag, Auth, Role


class LoginFrom(FlaskForm):
    """管理员登录表单"""
    account = StringField(
        label='账号',
        validators=[
            DataRequired('请输入账号！')
        ],
        description='账号',
        render_kw={
            'class': "form-control",
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
            'class': "form-control",
            'placeholder': "请输入密码",
            'required': "required"
        }
    )
    submit = SubmitField(
        label='登录',
        render_kw={
            'class': "btn btn-primary btn-block btn-flat"
        }
    )

    def validate_account(self, field):
        """从Admin数据库中，检测账号是否存在，如果不存在则在account.errors中添加错误信息"""
        account = field.data
        admin_num = Admin.query.filter_by(name=account).count()
        if admin_num == 0:
            raise ValidationError('账号不存在')


class TagForm(FlaskForm):
    name = StringField(
        label='名称',
        validators=[
            DataRequired('标签名称不能为空！')
        ],
        description='标签',
        render_kw={
            'class': "form-control",
            'id': "input_name",
            'placeholder': "请输入标签名称！"
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            'class': "btn btn-primary"
        }
    )


class MovieForm(FlaskForm):
    title = StringField(
        label='片名',
        validators=[
            DataRequired('请输入片名！')
        ],
        description='片名',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入标签名称！"
        }
    )
    url = FileField(
        label='电影文件',
        validators=[
            DataRequired('请上传电影文件！')
        ],
        description='电影文件',
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
    logo = FileField(
        label='封面',
        validators=[
            DataRequired('请上传封面！')
        ],
        description='封面',
    )
    star = SelectField(
        label='星级',
        validators=[
            DataRequired('请选择星级！')
        ],
        description='星级',
        coerce=int,
        choices=[(1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')],
        render_kw={
            'class': "form-control"
        }
    )
    tag_id = SelectField(
        label='标签',
        validators=[
            DataRequired('请选择标签！')
        ],
        coerce=int,
        # choices=[(tag.id, tag.name) for tag in Tag.query.all()],
        description='标签',
        render_kw={
            'class': "form-control"
        }
    )

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        self.tag_id.choices = [(v.id, v.name) for v in Tag.query.all()]

    area = StringField(
        label='上映地区',
        validators=[
            DataRequired('请输入上映地区！')
        ],
        description='上映地区',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入上映地区！"
        }
    )
    length = StringField(
        label='播放时长(分钟)',
        validators=[
            DataRequired('请输入播放时长！')
        ],
        description='播放时长',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入播放时长！",
        }
    )
    release_time = StringField(
        label='上映时间',
        validators=[
            DataRequired('请选择上映时间！')
        ],
        description='上映时间',
        render_kw={
            'class': "form-control",
            'placeholder': "请选择上映时间！",
            'id': "input_release_time"  # 由于使用了时间控件，需要指定id
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            'class': "btn btn-primary"
        }
    )


class PreviewForm(FlaskForm):
    title = StringField(
        label='预告标题',
        validators=[
            DataRequired('请输入预告标题！')
        ],
        description='请输入预告标题！',
        render_kw={
            'class': "form-control"
        }
    )
    logo = FileField(
        label='预告封面',
        validators=[
            DataRequired('请上传预告封面！')
        ],
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            'class': "btn btn-primary"
        }
    )


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label='旧密码',
        validators=[
            DataRequired('请输入旧密码！')
        ],
        description='旧密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入旧密码",
            'required': "required"
        }
    )
    new_pwd = PasswordField(
        label='新密码',
        validators=[
            DataRequired('请输入新密码！')
        ],
        description='新密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入新密码",
            'required': "required"
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            'class': "btn btn-primary"
        }
    )

    def validate_old_pwd(self, field):
        """检查验证旧密码是否正确"""
        from flask import session
        old_pwd = field.data
        login_name = session['login_admin']
        admin = Admin.query.filter_by(name=login_name).first()
        if not admin.check_pwd(old_pwd):
            raise ValidationError('旧密码错误！')


class AuthForm(FlaskForm):
    name = StringField(
        label='权限名称',
        validators=[
            DataRequired('请输入权限名称！')
        ],
        description='请输入权限名称！',
        render_kw={
            'class': "form-control"
        }
    )
    url = StringField(
        label='访问链接',
        validators=[
            DataRequired('请输入访问链接！')
        ],
        description='请输入访问链接！',
        render_kw={
            'class': "form-control",
            'placeholder': '链接地址'
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            'class': "btn btn-primary"
        }
    )


class RoleForm(FlaskForm):
    name = StringField(
        label='角色名称',
        validators=[
            DataRequired('请输入角色名称！')
        ],
        description='请输入角色名称！',
        render_kw={
            'class': "form-control"
        }
    )
    auths = SelectMultipleField(
        label='权限列表',
        description='请选择权限列表！',
        render_kw={
            'class': "form-control",
        },
        coerce=int,
        # choices=[(item.id, item.name) for item in Auth.query.all()]
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            'class': "btn btn-primary"
        }
    )

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.auths.choices = [(item.id, item.name) for item in Auth.query.all()]


class AdminForm(FlaskForm):
    name = StringField(
        label='管理员名称',
        validators=[
            DataRequired('请输入管理员名称！')
        ],
        description='管理员名称',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入管理员名称",
            'required': "required"
        }
    )

    pwd = PasswordField(
        label='管理员密码',
        validators=[
            DataRequired('请输入管理员密码！')
        ],
        description='管理员密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入管理员密码",
            'required': "required"
        }
    )
    repwd = PasswordField(
        label='管理员重复密码',
        validators=[
            DataRequired('请输入管理员重复密码！'),
            EqualTo('pwd', message='两次密码不一致')
        ],
        description='管理员重复密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入管理员重复密码",
            'required': "required"
        }
    )
    is_super = SelectField(
        label='星级',
        validators=[
            DataRequired('请选择星级！')
        ],
        description='星级',
        coerce=int,
        choices=[(1, '普通管理员'), (0, '超级管理员')],
        render_kw={
            'class': "form-control"
        }
    )
    role_id = SelectField(
        label='所属角色',
        validators=[
            DataRequired('请选择所属角色！')
        ],
        coerce=int,
        # choices=[(role.id, role.name) for role in Role.query.all()],
        description='所属角色',
        render_kw={
            'class': "form-control"
        }
    )

    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
        self.role_id.choices = [(v.id, v.name) for v in Role.query.all()]

    submit = SubmitField(
        label='提交',
        render_kw={
            'class': "btn btn-primary"
        }
    )
