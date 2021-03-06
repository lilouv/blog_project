from flask import Flask, render_template, request
from admin.admin import admin as admin_blueprint
from article.article import article as article_blueprint
import config, os
from models import User, db, Article, ArticleGroup

app = Flask(__name__)
app.register_blueprint(admin_blueprint)
app.register_blueprint(article_blueprint)
app.config.from_object(config)
db.init_app(app)

if not os.path.exists(os.path.join(os.path.dirname(__file__), 'blog.db')):
    db.create_all(app=app)

@app.route('/index')
@app.route('/')
def index():
    page = int(request.args.get('page', default=1))
    paginate = Article.query.order_by(Article.create_time.desc()).paginate(page=page, per_page=5)
    articles = paginate.items
    groups = ArticleGroup.query.all()
    return render_template('index.html', groups=groups, articles=articles, paginate=paginate)

if __name__ == '__main__':
    app.run(debug=True)
