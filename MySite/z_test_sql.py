from MySite.database import db_session
from MySite.models import User, Diary
import datetime
import time

# d = Diary('admin', 'admin@localhost')
# db_session.add(d)
# db_session.commit()


def inset(content=None, address=None, state=None, create_time=None, modify_time=None):
    d = Diary(content, address, state, create_time, modify_time)
    db_session.add(d)
    db_session.commit()
    pass


if __name__ == '__main__':
    data = {'CreateTime': '2020-03-03', 'Content': '这是我的第二篇日记', 'State': 1, 'Address': '河南省内乡县', 'ModifyTime': '2020-03-03 12:34:57'}
    inset(content=data['content'], address=data['address'], state=data['state'], create_time=data['create_time'], modify_time=data['modify_time'])