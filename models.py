from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    head_url = db.Column(db.String(255), default='/static/imgs/default.jpg')
    nickname = db.Column(db.String(32), default='')
    age = db.Column(db.String(32), default=0)
    
    def __repr__(self):
        return '<User %s>' % self.username


class ArticleGroup(db.Model):
    __tablename__ = 'article_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    color = db.Column(db.String(32), nullable=False)
    uid = db.Column(db.Integer)

    def __repr__(self):
        return '<ArticleGroup %s>' % self.name

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    gid = db.Column(db.Integer, db.ForeignKey('article_group.id'))
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    user = db.relationship("User", backref=db.backref("articles"))
    group = db.relationship("ArticleGroup", backref=db.backref("articles"))
    articalimg = db.Column(db.String(100), default="/static/imgs/article_df.png")
    articalvideo = db.Column(db.String(200))
    uuid = db.Column(db.String(255), unique=True)
    starcnt =  db.Column(db.Integer,default=0)

    def __repr__(self):
        return '<Article %s>' % self.title


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"))
    to_uid = db.Column(db.Integer, db.ForeignKey("user.id"))
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"))
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime)
    is_reply = db.Column(db.Integer, nullable=False)
    root = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", foreign_keys=uid)
    to_user = db.relationship("User", foreign_keys=to_uid)


class Star(db.Model):
    __tablename__ = 'star'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer)
    article_id = db.Column(db.Integer)


class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer)
    article_id = db.Column(db.Integer)

