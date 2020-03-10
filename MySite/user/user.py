from flask import Blueprint
from flask import request, session, jsonify, abort
from flask_login import login_required, login_user
from flask_httpauth import HTTPBasicAuth
from MySite.models import db, User, Diary
from MySite.app import create_app
from MySite.app import load_user


# 创建蓝图
users = Blueprint('user', __name__, url_prefix='/users')
# # 实例化HTTPBasicAuth，添加login_required装饰器
# auth = HTTPBasicAuth()


# 注册用户
@users.route('/register', methods=['POST'])
def register():
    username = request.get_json(force=True)['username']
    password = request.get_json(force=True)['password']
    # print(username, password)
    if username is None or password is None:
        if username is None:
            return jsonify({"msg": "用户名不能为空"})
        elif password is None:
            return jsonify({"msg": "密码不能为空"})
    if db.session.query(User).filter(User.UserName == username).first() is not None:
        return jsonify({"msg": "用户名已存在"})
    user = User(username=username)
    user.hash_password(password)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"msg": "register error."})
    return jsonify({"uid": user.id, "username": user.UserName, "msg": "success"})


# 登录
@users.route('/login', methods=['POST'])
def login():
    username = request.get_json(force=True)['username']
    password = request.get_json(force=True)['password']
    if username is None or password is None:
        if username is None:
            return jsonify({"msg": "用户名不能为空"})
        if db.session.query(User).filter(User.UserName == username).first() is None:
            return jsonify({"msg": "该用户不存在"})
        if password is None:
            return jsonify({"msg": "密码不能为空"})
    else:
        # 查询用户验证密码
        user = User(username=username).verify_password(password)
    if user:
        login_user(user)
        return jsonify({'msg': 'Login Success.', 'user_id': User.get_id()})
    else:
        return jsonify({'msg': 'Login Error.'})


# 查询
@users.route('/api/v1', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def user():
    if request.method == 'GET':
        data = request.get_json(force=True)
        # print(data)
        # 条件过滤
        filterList = []
        # diary状态
        if data['username'] is not None:
            filterList.append(User.UserName == data['username'])
        # print(filterList)
        user_ob = db.session.query(User).filter(*filterList).all()
        user_list = []
        for u in user_ob:
            info = {}
            info['id'] = u.id
            info['username'] = u.UserName
            info['registertime'] = u.RegisterTime.strftime('%Y-%m-%d %H:%M:%S')
            user_list.append(info)
        result = {'msg': 'success', 'user_list': user_list, 'ip': request.remote_addr}
        return jsonify(result)
        pass


@users.route('/api/v1/<int:u_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def user_info(u_id):
    if request.method == 'GET':
        # print(u_id)
        user_ob = db.session.query(User).filter(User.id == u_id).first()
        return jsonify({"username": user_ob.UserName, "register_time": user_ob.RegisterTime})
        pass
