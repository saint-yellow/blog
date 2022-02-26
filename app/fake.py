import random

from faker import Faker

from app.models import Article, Comment, db

faker = Faker()


def make_articles(count=100):
    for i in range(count):
        a = Article(title=faker.name(), body=faker.text(), timestamp=faker.past_date())
        db.session.add(a)
    db.session.commit()


def make_comments_after_articles(count=100):
    articles_count = Article.query.count()
    for i in range(count):
        article_id = random.randint(1, articles_count)
        article = Article.query.filter_by(id=article_id).first()
        c = Comment(nickname=faker.name(), email=faker.email(), body=faker.text(), timestamp=faker.past_date(), article=article)
        db.session.add(c)
    db.session.commit()


def make_comments_after_comments(count=100):
    ...
