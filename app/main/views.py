from app.main.forms import CommentForm
from app.models import Article, Comment, db
from flask import flash, redirect, render_template, request, url_for

from . import main


@main.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(
        page, per_page=10, error_out=False
    )
    articles = pagination.items
    return render_template('index.html', articles=articles, pagination=pagination)


@main.route('/article/<int:id>', methods=['GET', 'POST'])
def article(id: int):
    article = Article.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(nickname=form.nickname.data, body=form.body.data, article=article)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('main.article', id=article.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (article.comments.count() - 1) // 10 + 1
    pagination = article.comments.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=10, error_out=False,
    )
    comments = pagination.items
    return render_template('article.html', article=article, form=form, comments=comments, pagination=pagination)
