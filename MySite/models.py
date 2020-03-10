from passlib.apps import custom_app_context as pwd_context
from MySite.app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(50), unique=True)
    PassWord = db.Column(db.String(128))
    RegisterTime = db.Column(db.TIMESTAMP, nullable=False)
    diaries = db.relationship("Diary")

    def __init__(self, username=None, password=None, register_time=None):
        self.UserName = username
        self.PassWord = password
        self.RegisterTime = register_time

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def hash_password(self, password):
        self.PassWord = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.PassWord)

    def __repr__(self):
        return '<User %r>' % (self.UserName)


# 日记
class Diary(db.Model):
    __tablename__ = 'diary'
    id = db.Column(db.Integer, primary_key=True)
    Content = db.Column(db.Text)  # 日记内容
    Address = db.Column(db.String(50), server_default=None)  # 地址
    State = db.Column(db.Enum('1', '0'), server_default='1')
    CreateTime = db.Column(db.Date, nullable=False)  # 创建时间
    UpdateTime = db.Column(db.TIMESTAMP, nullable=False)  # 更新时间
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # __table_arg__ = {
    #     'mysql_charset': 'utf8mb4'
    # }

    def __init__(self, content=None, address=None, state=None, create_time=None, update_time=None):
        self.Content = content
        self.Address = address
        self.State = state
        self.CreateTime = create_time
        self.UpdateTime = update_time

    # def __repr__(self):
    #     data = "{'cid': '%s', 'Content': '%s', 'Address': '%s', 'State': '%s', 'CreateTime': '%s', 'ModifyTime': '%s'}" %\
    #            (self.id, self.Content, self.Address, self.State, self.CreateTime, self.ModifyTime)
    #     print(type(data))
    #     return data

