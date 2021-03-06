import datetime
import os
import json
import uuid
from PIL import Image
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from models import User, db, Article, ArticleGroup, Comment, Favorite, Star
from utils import login_check
from werkzeug.utils import secure_filename

article = Blueprint('article', __name__, url_prefix='/article', template_folder='views')


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','mp4'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@article.route('/index')
@article.route('/')
def index():
    page = int(request.args.get('page', default=1))
    paginate = Article.query.order_by(Article.create_time.desc()).paginate(page=page, per_page=5)
    articles = paginate.items
    groups = ArticleGroup.query.all()
    return render_template('index.html', groups=groups, articles=articles, paginate=paginate)

@article.route('/article_detail/<int:article_id>')
def article_detail(article_id):
    article = Article.query.get(article_id)
    current_time = article.create_time
    prev_article = Article.query.filter(Article.create_time>current_time).all()
    next_article = Article.query.filter(Article.create_time<current_time).all()
    
    if prev_article:
        prev_article = prev_article[0]
    if next_article:
        next_article = next_article[-1]

    if 'uid' in session:
        groups = ArticleGroup.query.filter_by(uid=session['uid']).all()
    else:
        groups = None
    print(article.articalvideo)
    comments = Comment.query.filter_by(article_id=article_id).all()
    return render_template('article_detail.html', article=article, prev_article=prev_article, next_article=next_article, groups=groups, comments=comments)

@article.route('/group_articles/<int:gid>')
def group_articles(gid):
    page = int(request.args.get('page', default=1))
    group = ArticleGroup.query.get(gid)
    paginate = Article.query.filter_by(gid=group.id).paginate(page=page, per_page=5)
    articles = paginate.items
    groups = ArticleGroup.query.all()
    return render_template('group_articles.html', group=group, paginate=paginate, articles=articles, groups=groups)

@article.route('/add_article', methods=['GET', 'POST'])
@login_check
def add_article():
    if request.method == 'GET':
        groups = ArticleGroup.query.filter_by(uid=session['uid']).all()
        return render_template('add_article.html', groups=groups)
    elif request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        gid = request.form.get('gid')
        filepath = ''
        f = request.files['file']
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            filepath = os.path.join(current_app.config['UPLOAD_PATH'], fname)
            print('filepath:{}'.format(filepath))
            f.save(filepath)
        filepath2 = ''
        f2 = request.files['file2']
        if f2 and allowed_file(f2.filename):
            f2name = secure_filename(f2.filename)
            filepath2 = os.path.join(current_app.config['UPLOAD_PATH'], f2name)
            print('filepath2:{}'.format(filepath2))
            f2.save(filepath2)
        user = User.query.filter_by(username=session.get('user')).first()
        uid = user.id
        create_time = datetime.datetime.now()

        article = Article()
        article.title = title
        article.content = content
        article.gid = gid
        article.uid = uid
        if filepath:
            article.articalimg = "/" + filepath
        if filepath2:
            article.uuid=uuid.uuid4().hex
            article.articalvideo= "/" + filepath2[15:]

        article.create_time = create_time

        try:
            db.session.add(article)
            db.session.commit()
            flash('添加文章%s成功' % title, 'success')
            return redirect(url_for('article.add_article'))
        except Exception as e:
            print(e)
            flash('添加文章%s失败' % title, 'danger')
            return redirect(url_for('article.add_article'))

@article.route('/add_group', methods=['GET', 'POST'])
@login_check
def add_group():
    if request.method == 'GET':
        groups = ArticleGroup.query.filter_by(uid=session['uid']).all()
        colors = ['default', 'primary', 'success', 'info', 'warning', 'danger']
        return render_template('add_group.html', colors=colors, groups=groups)
    elif request.method == 'POST':
        name = request.form.get('name')
        color = request.form.get('color')

        group = ArticleGroup()
        group.name = name
        group.color = color
        group.uid = session['uid']

        try:
            db.session.add(group)
            db.session.commit()
            flash('添加分组成功', 'success')
            return redirect(url_for('article.article_group_manage'))
        except Exception as e:
            print('Exception: {}'.format(e))
            flash('添加分组失败', 'danger')
            return redirect(url_for('article.article_group_manage'))

@article.route('/article_group_manage')
@login_check
def article_group_manage():
    page = int(request.args.get('page', default=1))
    if session['user'] != 'admin':
        paginate = ArticleGroup.query.filter_by(uid=session['uid']).paginate(page=page, per_page=5)
        groups = ArticleGroup.query.filter_by(uid=session['uid']).all()
    else:
        paginate = ArticleGroup.query.paginate(page=page, per_page=5)
        groups = ArticleGroup.query.all()
    groups_table = paginate.items
    
    return render_template('article_group_manage.html', groups_table=groups_table, paginate=paginate, groups=groups)

@article.route('/edit_group/<int:gid>', methods=['GET', 'POST'])
@login_check
def edit_group(gid):
    if request.method == 'GET':
        groups = ArticleGroup.query.filter_by(uid=session['uid']).all()
        group = ArticleGroup.query.get(gid)
        colors = ['default', 'primary', 'success', 'info', 'warning', 'danger']
        return render_template('edit_group.html', group=group, colors=colors, groups=groups)
    elif request.method == 'POST':
        name = request.form.get('name')
        color = request.form.get('color')

        group = ArticleGroup.query.get(gid)
        group.name = name
        group.color = color

        try:
            db.session.commit()
            flash('修改成功', 'success')
            return redirect(url_for('article.article_group_manage'))
        except Exception:
            flash('修改失败', 'danger')
            return redirect(url_for('article.article_group_manage'))

@article.route('/delete_group/<int:gid>')
@login_check
def delete_group(gid):
    group = ArticleGroup.query.get(gid)
    try:
        db.session.delete(group)
        db.session.commit()
        flash('删除%s成功' % group.name, 'success')
        return redirect(url_for('article.article_group_manage'))
    except Exception:
        flash('删除%s失败' % group.name, 'danger')
        return redirect(url_for('article.article_group_manage'))

@article.route('/article_manage')
@login_check
def article_manage():
    username = session.get('user')
    user = User.query.filter_by(username=username).first()
    page = int(request.args.get('page', default=1))
    if session['user'] != 'admin':
        paginate = Article.query.filter_by(uid=user.id).paginate(page=page, per_page=5)
        groups = ArticleGroup.query.filter_by(uid=session['uid']).all()
    else:
        paginate = Article.query.paginate(page=page, per_page=5)
        groups = ArticleGroup.query.all()
    articles = paginate.items
    
    return render_template('article_manage.html',articles=articles, groups=groups, paginate=paginate)


@article.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
@login_check
def edit_article(article_id):
    if request.method == 'GET':
        article = Article.query.get(article_id)
        groups = ArticleGroup.query.filter_by(uid=session['uid']).all()
        return render_template('edit_article.html', groups=groups, article=article)
    elif request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        gid = request.form.get('gid')
        update_time = datetime.datetime.now()
        
        article = Article.query.get(article_id)
        articalimg = article.articalimg
        f = request.files['file']
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            filepath = os.path.join(current_app.config['UPLOAD_PATH'], fname)
            print('filepath:{}'.format(filepath))
            f.save(filepath)
            articalimg = "/" + filepath
        filepath2 = ''
        f2 = request.files['file2']
        if f2 and allowed_file(f2.filename):
            f2name = secure_filename(f2.filename)
            filepath2 = os.path.join(current_app.config['UPLOAD_PATH'], f2name)
            f2.save(filepath2)
            
        article.title = title
        article.content = content
        article.gid = gid
        article.update_time = update_time
        article.articalimg = articalimg
        if filepath2:
            article.uuid=uuid.uuid4().hex
            article.articalvideo= "/" + filepath2[15:]

        try:
            db.session.commit()
            flash('修改文章%s成功' % title, 'success')
            return redirect(url_for('article.article_manage'))
        except Exception:
            flash('修改文章%s失败' % title, 'danger')
            return redirect(url_for('article.article_manage'))

@article.route('/delete_article/<int:article_id>')
@login_check
def delete_article(article_id):
    article = Article.query.get(article_id)
    try:
        db.session.delete(article)
        db.session.commit()
        flash('删除文章%s成功' % article.title, 'success')
        return redirect(url_for('article.article_manage'))
    except Exception:
        flash('删除文章%s失败' % article.title, 'danger')
        return redirect(url_for('article.article_manage'))

@article.route('/add_comment/<username>/<int:to_uid>/<int:article_id>/<int:is_reply>/<int:root>', methods=['GET', 'POST'])
@login_check
def add_comment(username, to_uid, article_id, is_reply, root):
    if request.method == 'GET':
        return render_template('add_comment.html', username=username, to_uid=to_uid, article_id=article_id, is_reply=is_reply, root=root)
    elif request.method == 'POST':
        user = User.query.filter_by(username=username).first()
        content = request.form.get('content')

        comment = Comment()
        comment.uid = user.id
        comment.to_uid = to_uid
        comment.article_id = article_id
        comment.content = content
        comment.create_time = datetime.datetime.now()
        comment.is_reply = is_reply
        comment.root = root

        try:
            db.session.add(comment)
            db.session.commit()
            flash('添加评论成功', 'success')
            return redirect(url_for('article.article_detail', article_id=article_id))
        except Exception:
            flash('添加评论失败', 'danger')
            return redirect(url_for('article.article_detail', article_id=article_id))


@article.route('/upload_head', methods=['GET', 'POST'])
@login_check
def upload_head():
    avatar_src = request.form.get('avatar_src')
    avatar_data = request.form.get('avatar_data')
    avatar_file = request.files['avatar_file']

    print('-'*50)
    print(avatar_src)
    print(avatar_data)
    print(avatar_file)
    print('-' * 50)

    avatar_file.save('static/uploads/%s' % avatar_file.filename)

    avatar_data = json.loads(avatar_data)

    x = avatar_data.get('x')
    y = avatar_data.get('y')
    h = avatar_data.get('height')
    w = avatar_data.get('width')
    r = avatar_data.get('rotate')

    img = Image.open("static/uploads/%s" % avatar_file.filename)

    # 旋转图片
    if r == 90:
        img = img.transpose(Image.ROTATE_90)
    elif r == 180:
        img = img.transpose(Image.ROTATE_180)
    elif r == 270:
        img = img.transpose(Image.ROTATE_270)

    region = img.crop((x, y, x + w, y + h))
    region.save("static/uploads/crop_%s" % avatar_file.filename)

    # 保存用户头像图片链接
    username = session.get('user')
    user = User.query.filter_by(username=username).first()
    user.head_url = "/static/uploads/crop_%s" % avatar_file.filename
    db.session.commit()

    return jsonify({
        'result': '/static/uploads/crop_%s' % avatar_file.filename
    })


@article.route('/my_article')
@login_check
def my_article():
    page = int(request.args.get('page', default=1))
    username = session.get('user')
    user = User.query.filter_by(username=username).first()
    paginate = Article.query.filter_by(uid=user.id).paginate(page=page, per_page=5)
    articles = paginate.items
    groups = ArticleGroup.query.filter_by(uid = session['uid']).all()
    return render_template('my_article.html', paginate=paginate, articles=articles, groups=groups)


@article.route('/upload_editor_img', methods=['GET', 'POST'])
def upload_editor_img():
    try:
        img = request.files['editormd-image-file']
        uuidstr = ''.join(uuid.uuid4().__str__().split('-'))
        filename = '%s%s' % (uuidstr, img.filename)
        img.save('static/uploads/%s' % filename)

        result = {
            'success': 1,
            'message': '上传成功',
            'url': '/static/uploads/%s' % filename
        }
        return json.dumps(result)
    except Exception as e:
        print(e)
        result = {
            'success': 0,
            'message': '上传失败',
        }
        return json.dumps(result)


@article.route('/favorite')
@login_check
def favorite():
    uid = session['uid']
    favorites = Favorite.query.filter_by(uid = uid).all()
    articles = Article.query.filter(Article.id.in_([item.article_id for item in favorites])).all()
    return render_template('favorite_manage.html', articles=articles)

@article.route('/favorite/add/<article_id>')
@login_check
def favorite_add(article_id):
    uid = session['uid']
    favorite = Favorite.query.filter_by(article_id = article_id, uid = uid).first()
    if favorite:
        flash('已经收藏，无需再收藏', 'danger')
        return redirect(url_for('article.article_detail',article_id=article_id ))
    else:
        favorite = Favorite()
        favorite.article_id = article_id
        favorite.uid = uid
        db.session.add(favorite)
        db.session.commit()
        flash('收藏成功', 'success')
        return redirect(url_for('article.article_detail',article_id=article_id ))

@article.route('/favorite/delete/<favorite_id>')
@login_check
def favorite_delete(favorite_id):
    uid = session['uid']
    favorite = Favorite.query.filter_by(id = favorite_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        flash('删除收藏成功', 'success')
    return redirect(url_for('article.favorite'))

@article.route('/star/<article_id>')
@login_check
def star(article_id):
    uid = session['uid']
    star = Star.query.filter_by(article_id=article_id, uid=uid).first()
    article  = Article.query.filter_by(id=article_id).first()
    if star:
        flash('撤销点赞', 'danger')
        article.starcnt -= 1
        db.session.delete(star)
        db.session.commit()
        return redirect(url_for('article.article_detail',article_id=article_id ))
    else:
        star = Star()
        star.article_id = article_id
        star.uid = uid
        article.starcnt += 1
        db.session.add(star)
        db.session.commit()
        flash('点赞成功', 'success')
        return redirect(url_for('article.article_detail',article_id=article_id ))