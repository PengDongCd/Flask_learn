from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Dong Peng'}
    posts = [
        {
            'author': {'username': '刘'},
            'body': '这是模板模块中的循环例子～1'

        },
        {
            'author': {'username': '忠强'},
            'body': '这是模板模块中的循环例子～2'
        }
    ]
    return render_template('index.html', title='My', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 判断当前的用户是否经过了授权，如果是的话直接返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    # 对表格数据进行验证
    if form.validate_on_submit():
        # 根据表格里面的数据进行查询，如果查询到user就返回user对象，否则返回None
        user = User.query.filter_by(username=form.username.data).first()
        # 判断用户是否存在或者密码是否正确
        if user is None or not user.check_password(form.password.data):
            # 如果用户不存在或者密码不正确就闪现错误信息
            flash('无效的用户名或者密码')
            # 然后重新定位到登录页面
            return redirect(url_for('login'))
        # 利用这个方法，当用户名和密码都正确解决是否要记住用户登录状态的问题
        login_user(user, remember=form.remember_me.data)
        # 此时的next记录的是跳转至登录页面时的地址
        next_page = request.args.get('next')

        # 如果next_page记录的地址不存在就返回首页
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='登 录', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你成为我们网站的新用户!')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': '测试Post #1号'},
        {'author': user, 'body': '测试Post #2号'}
    ]

    return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('你的提交已经变更！')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='个人资料编辑',
                           form=form)
