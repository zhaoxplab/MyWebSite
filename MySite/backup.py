from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# 实例化SQLAlchemy
db = SQLAlchemy()
# 实例化LoginManager
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    # SQLAlchemy注册
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:100798@47.97.166.98:3306/zhaoxp?charset=utf8mb4'
    # 设置数据库追踪信息，压制警告
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    login_manager.init_app(app)

    # 蓝图注册
    from MySite.diary.diary import diary
    from MySite.user.user import users
    app.register_blueprint(diary)
    app.register_blueprint(users)
    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=8000, debug=True)