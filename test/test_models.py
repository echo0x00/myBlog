import pytest
from models.models import User, Post, Category, prepare_session, fill_db, delete_db_file


@pytest.fixture(scope="function")
def session_with_empty_db():
    delete_db_file()
    yield prepare_session()
    delete_db_file()


@pytest.fixture(scope="function")
def session_with_populated_db():
    delete_db_file()
    session = prepare_session()
    fill_db(session())
    yield prepare_session()
    delete_db_file()


def test_add_user_to_db(session_with_empty_db):
    user = User(name='Alex Black',
                email='alex@black.com',
                password='PaSsAlex')
    session = session_with_empty_db()
    session.add(user)
    session.commit()
    user_from_db = session.query(User).filter_by(name='Alex Black').first()
    assert (user_from_db.name, user_from_db.email, user_from_db.password) == (
        'Alex Black', 'alex@black.com', 'PaSsAlex')


def test_get_posts_created_by_user(session_with_populated_db):
    session = session_with_populated_db()
    user = session.query(User).filter_by(name='Alex Green').first()
    assert len(user.posts) == 2


def test_get_post(session_with_populated_db):
    session = session_with_populated_db()
    post = session.query(Post).filter_by(id=1).first()
    assert post.title == 'Пост про програмистов, которые программируют'


def test_get_cat_of_post(session_with_populated_db):
    session = session_with_populated_db()
    post = session.query(Post).filter_by(title='Пост про програмистов, которые программируют').first()
    assert len(post.cats) == 1


def test_add_cat_to_post(session_with_populated_db):
    session = session_with_populated_db()
    cat = Category(title='Testers')
    session.add(cat)
    session.commit()
    post = session.query(Post).filter_by(title='Пост про дизайнеров и архитекторов').first()
    post.cats.append(cat)
    session.commit()
    assert len(post.cats) == 2

