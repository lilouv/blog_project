# 基于Flask实现简单的博客系统
## 介绍
这是用flask写的简单的博客系统。

功能：用户注册、头像上传、资料修改、支持Markdown编辑、博客的删除和修改、评论、点赞、收藏、博客可添加分类及封面、支持上传视频(可发弹幕)、后台管理


## 项目结构
```python
—— blog 
     |—— admin # 蓝图目录
           |—— views # html模板目录
                 |——...
           |—— admin.py # url 视图文件
     |—— article # 蓝图目录 
           |—— views # html模板目录
                 |——...
           |—— admin.py # url 视图文件                
     |—— static # 静态文件目录
     |—— templates # html模板目录
           |——...
     |—— app.py # 主文件
     |—— config.py # 配置文件
     |—— models.py # 数据类
     |—— utils.py # 辅助类
     |—— README.md # 说明
```
## 展示
![图片1](https://img-blog.csdnimg.cn/20210306120155241.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xpbmtlZXA=,size_16,color_FFFFFF,t_70)

![图片2](https://img-blog.csdnimg.cn/20210306120155450.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xpbmtlZXA=,size_16,color_FFFFFF,t_70)

## 程序实现
### 前端页面
使用bootstrap美化页面样式

```python
<link rel="stylesheet" href="/static/css/bootstrap.min.css">
<script src="/static/js/jquery.js"></script>
<script src="/static/js/bootstrap.min.js"></script>
```
### 后端部分程序
注册

```python
@admin.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST'
			...
            try:
                db.session.add(user)
                db.session.commit()
                flash('注册成功', 'success')
                return redirect(url_for('admin.register'))
            except Exception:
                flash('注册失败', 'danger')
                return redirect(url_for('admin.register'))
        else:
            flash('注册失败', 'danger')
            return redirect(url_for('admin.register'))
```
添加分组

```python
@article.route('/add_group', methods=['GET', 'POST'])
@login_check
def add_group():
    if request.method == 'GET':
        groups = ArticleGroup.query.filter_by(uid=session['uid']).all()
        colors = ['default', 'primary', 'success', 'info', 'warning', 'danger']
        return render_template('add_group.html', colors=colors, groups=groups)
    elif request.method == 'POST':
		...
        try:
            db.session.add(group)
            db.session.commit()
            flash('添加分组成功', 'success')
            return redirect(url_for('article.article_group_manage'))
        except Exception as e:
            print('Exception: {}'.format(e))
            flash('添加分组失败', 'danger')
            return redirect(url_for('article.article_group_manage'))
```

评论

```python
@article.route('/add_comment/<username>/<int:to_uid>/<int:article_id>/<int:is_reply>/<int:root>', methods=['GET', 'POST'])
@login_check
def add_comment(username, to_uid, article_id, is_reply, root):
    if request.method == 'GET':
        return render_template('add_comment.html', username=username, to_uid=to_uid, article_id=article_id, is_reply=is_reply, root=root)
    elif request.method == 'POST':
    	...
        try:
            db.session.add(comment)
            db.session.commit()
            flash('添加评论成功', 'success')
            return redirect(url_for('article.article_detail', article_id=article_id))
        except Exception:
            flash('添加评论失败', 'danger')
            return redirect(url_for('article.article_detail', article_id=article_id))
```

### 权限管理
自定义类装饰器
```python
# 管理员验证
def rule_check(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not session.get('user') == 'admin':
            flash('你没有权限访问,请使用管理员账号登录！', 'warning')
            return redirect(url_for('admin.manage'))
        return func(*args, **kwargs)
    return inner

```
### 第三方组件
使用editor.md 实现Markdown编辑器
使用Dplayer 实现视频播放、添加弹幕
使用html5 头像上传更换插件实现头像上传

## 遇到的困难
常常忘记加上methods=['GET', 'POST']
刚开始对前端页面没什么思路，后来了解了一下bootstrap
做到支持Markdown和头像上传时，以为会很困难，后来发现有第三方组件可以用，
想了想还是偷懒吧

