from MySite.models import db
from MySite.app import create_app


def init_db():
    # 创建
    db.create_all(app=create_app())


def drop_db():
    # 删除
    db.drop_all(app=create_app())


if __name__ == '__main__':
    drop_db()
    init_db()
    print('success')
