from flask import Blueprint
from flask import request, jsonify
from MySite.models import db, Diary
import time

# 创建蓝图
diary = Blueprint('diary', __name__, url_prefix='/diary')


@diary.route('/')
def index():
    return '<h1>Hello, this is admin blueprint</h1>'


# 新建日迹
@diary.route('/api/v1', methods=['GET', 'POST', 'PUT', 'DELETE'])
def diary_list():
    if request.method == 'GET':
        """
        查询视图
        
        """
        data = request.get_json(force=True)
        print(data)
        # 条件过滤
        filterList = []
        # diary状态
        if data['state'] is not None:
            filterList.append(Diary.State == data['state'])
        if data['cid'] is not None:
            filterList.append(Diary.id == str(data['cid']))
        if data['create_time'] is not None:
            filterList.append(Diary.id == str(data['create_time']))
        # print(filterList)
        diary_ob = db.session.query(Diary).filter(*filterList).all()
        diary_list = []
        for d in diary_ob:
            info = {}
            info['cid'] = d.id
            info['Content'] = d.Content
            info['Address'] = d.Address
            info['State'] = d.State
            info['CreateTime'] = d.CreateTime.strftime('%Y-%m-%d')
            info['UpdateTime'] = d.UpdateTime.strftime('%Y-%m-%d %H:%M:%S')
            diary_list.append(info)
        result = {'msg': 'success', 'diary_list': diary_list, 'ip': request.remote_addr}
        return jsonify(result)

    elif request.method == 'POST':
        data = request.get_json(force=True)
        content = data['content']
        address = data['address']
        state = data['state']
        create_time = time.strftime('%Y-%m-%d')
        diary_insert = Diary(content=content,
                             address=address,
                             state=state,
                             create_time=create_time)
        try:
            db.session.add(diary_insert)
            db.session.commit()
            info = {}
            info['Content'] = content
            info['CreateTime'] = create_time
            result = {'msg': 'success', 'data': info, 'ip': request.remote_addr}
            return jsonify(result)
        except Exception:
            return jsonify({"msg": "error"})

    elif request.method == 'PUT':
        data = request.get_json(force=True)
        return jsonify(data)
        pass

    elif request.method == 'DELETE':
        pass
    else:
        return jsonify({'state': 400})


# 获取单个
@diary.route('/api/v1/<int:diary_id>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def diary_one(diary_id):
    print(diary_id)
    if request.method == 'GET':
        diary_ob = db.session.query(Diary).filter(Diary.id == diary_id).first()
        return jsonify({"content": diary_ob.Content})
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
    else:
        return jsonify({'state': 400})


"""
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
"""
