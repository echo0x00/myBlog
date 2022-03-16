from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Text,
    Boolean,
    DateTime,
    Table
)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

import os.path
import pathlib

DB_FILE_NAME = 'my_blog.db'
DB_PATH = os.path.join(pathlib.Path().absolute(), 'db', DB_FILE_NAME)

engine = create_engine(f'sqlite:///{DB_PATH}')
Base = declarative_base(bind=engine)

bind_posts_cats = Table('posts_cats', Base.metadata,
                        Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
                        Column('cats_id', Integer, ForeignKey('cats.id'), primary_key=True)
                        )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(),
                        default=datetime.now,
                        onupdate=datetime.now)
    posts = relationship('Post', back_populates='user')

    def __repr__(self):
        return (f"<User(name='{self.name}', email='{self.email}',"
                f" password='{self.password}')>")


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(256), nullable=False)
    body = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_published = Column(Boolean, nullable=False, default=False)
    user = relationship('User', back_populates='posts', lazy='joined')
    cats = relationship('Category', secondary=bind_posts_cats, back_populates='posts')

    def __repr__(self):
        return f'Post №{self.id}. {self.title}'


class Category(Base):
    __tablename__ = 'cats'

    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False, unique=True, index=True)
    posts = relationship('Post', secondary=bind_posts_cats, back_populates='cats')

    def __repr__(self):
        return f'{self.title}'


def delete_db_file():
    if os.path.isfile(DB_PATH):
        os.remove(DB_PATH)


def fill_db(session):
    user_01 = User(name='Alex Green',
                   email='alex_001@gmail.com',
                   password='pass001')
    user_02 = User(name='Alex Blue',
                   email='alex_002@gmail.com',
                   password='pass002')
    user_03 = User(name='Alex Red',
                   email='alex_003@gmail.com',
                   password='pass003')

    session.add_all((user_01, user_02, user_03))
    session.flush()

    cat_01 = Category(title='Coders')
    cat_02 = Category(title='Designers')

    session.add_all((cat_01, cat_02))
    session.flush()

    post_01 = Post(title='Пост про програмистов, которые программируют',
                   body='Программисты пишут код буквами',
                   author_id=user_01.id)

    post_02 = Post(title='Пост про дизайнеров и архитекторов',
                   body='Как хорошо что есть дизайнеры',
                   author_id=user_01.id)

    post_03 = Post(title='Еще один пост про программистов',
                   body='Этот пост просто про програмистов которые нажимают на кнопки',
                   author_id=user_02.id)

    session.add_all((post_01, post_02, post_03))
    session.flush()

    post_01.cats.append(cat_01)
    post_02.cats.append(cat_02)
    post_03.cats.append(cat_01)

    session.commit()

    # print(post_01.cats)
    # print(post_02.user)

    # user = session.query(User).filter_by(name='Alex Green').first()
    # print(user)

    session.close()


def prepare_session():
    Base.metadata.create_all()
    return sessionmaker(bind=engine)
