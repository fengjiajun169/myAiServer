from datetime import datetime

from wxcloudrun import db


# 计数表
class Counters(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'Counters'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=1)
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())


# 问答表
class UserChatInfo(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'UserChatInfo'

    # 设定结构体对应表格的字段
    dt = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, primary_key=True)
    global_id = db.Column(db.BigInteger, primary_key=True)

    finish_time = db.Column('finish_time', db.TIMESTAMP, nullable=False, default=datetime.now())
    creat_time = db.Column('creat_time', db.TIMESTAMP, nullable=False, default=datetime.now())
    duration_time = db.Column(db.Integer, default=-1)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    status = db.Column(db.Integer, default=-1)