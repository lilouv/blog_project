from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import User, db, Article, ArticleGroup, Comment
from utils import login_check, rule_check
import hashlib

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='views')

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        user = User.query.filter_by(username=username, password=md5.hexdigest()).first()
        if user:
            session['user'] = username
            session['uid'] = user.id
            flash('登陆成功', 'success')
            return redirect(url_for('article.index'))
        else:
            flash('登陆失败', 'danger')
            return redirect(url_for('admin.login'))


@admin.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        check_password = request.form.get('check_password')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('用户已存在','danger')
            return redirect(url_for('admin.register'))
        if username and password and password == check_password:
            md5 = hashlib.md5()
            md5.update(password.encode('utf-8'))

            user = User()
            user.username = username
            user.password = md5.hexdigest()

            try:
                db.session.add(user)
                db.session.commit()
                flash('注册成功', 'success')
                return redirect(url_for('admin.login'))
            except Exception:
                flash('注册失败', 'danger')
                return redirect(url_for('admin.register'))
        else:
            flash('注册失败', 'danger')
            return redirect(url_for('admin.register'))


@admin.route('/logout')
def logout():
    session.clear()
    flash('注销登陆成功', 'success')
    return redirect(url_for('admin.login'))

@admin.route('/userinfo/<id>', methods=['GET', 'POST'])
@login_check
def userinfo(id):
    if request.method == 'GET':
        # username = session.get('user')
        user = User.query.get(id)
        groups = ArticleGroup.query.filter_by(uid=id).all()
        return render_template('userinfo.html', user=user, groups=groups)
    elif request.method == 'POST':
        nickname = request.form.get('nickname') or ''
        age = request.form.get('age') or ''
        username = session.get('user')
        user = User.query.get(id)
        user.nickname = nickname
        user.age = age

        try:
            db.session.commit()
            flash('修改成功', 'success')
            return redirect(url_for('admin.userinfo', id = id))
        except Exception:
            flash('修改失败', 'danger')
            return redirect(url_for('admin.userinfo', id = id))

@admin.route('/change_password', methods=['GET', 'POST'])
@login_check
def change_password():
    if request.method == 'GET':
        groups = ArticleGroup.query.all()
        return render_template('change_password.html', groups=groups)
    elif request.method == 'POST':
        username = session.get('user')
        user = User.query.filter_by(username=username).first()
        before_password = request.form.get('before_password')
        password = request.form.get('password')
        check_password = request.form.get('check_password')

        md5 = hashlib.md5()
        md5.update(before_password.encode('utf-8'))
        if user.password == md5.hexdigest() and password and check_password and password == check_password:

            md5 = hashlib.md5()
            md5.update(password.encode('utf-8'))
            user.password = md5.hexdigest()

            try:
                db.session.commit()
                flash('修改密码成功', 'success')
                return redirect(url_for('admin.change_password'))
            except Exception:
                flash('修改密码失败', 'danger')
                return redirect(url_for('admin.change_password'))
        else:
            flash('修改密码失败', 'danger')
            return redirect(url_for('admin.change_password'))

@admin.route('/manage')
@login_check
def manage():
    groups = ArticleGroup.query.all()
    return render_template('manage.html', groups=groups)


@admin.route('/user_manage')
@rule_check
@login_check
def user_manage():
    users = User.query.all()
    return render_template('user_manage.html', users=users)


@admin.route('/user/delete/<id>')
@rule_check
@login_check
def user_delete(id):
    user = User.query.get(id)
    articles = Article.query.filter_by(uid=id).all()
    groups = ArticleGroup.query.filter_by(uid=session['uid']).all()

    try:
        for article in articles:
            db.session.delete(article)
        for group in groups:
            db.session.delete(group)

        db.session.delete(user)
        db.session.commit()
        flash('删除%s成功' % user.username, 'success')
        return redirect(url_for('admin.user_manage'))
    except Exception:
        flash('删除%s失败' % user.username, 'danger')
        return redirect(url_for('admin.user_manage'))


@admin.route('/comment_manage')
@rule_check
@login_check
def comment_manage():
    comments = Comment.query.all()
    return render_template('comment_manage.html', comments=comments)

@admin.route('/comment/delete/<id>')
@rule_check
@login_check
def comment_delete(id):
    comment = Comment.query.get(id)
    try:
        db.session.delete(comment)
        db.session.commit()
        flash('删除评论成功' , 'success')
        return redirect(url_for('admin.user_manage'))
    except Exception:
        flash('删除评论失败', 'danger')
        return redirect(url_for('admin.user_manage'))