import logging

from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.model import Counters
from wxcloudrun.model import UserChatInfo

# 初始化日志
logger = logging.getLogger('log')


def query_counterbyid(id):
    """
    根据ID查询Counter实体
    :param id: Counter的ID
    :return: Counter实体
    """
    try:
        return Counters.query.filter(Counters.id == id).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def query_chatbyid(id):
    """
    根据ID查询Counter实体
    :param id: Chat的ID
    :return: Chat实体
    """
    try:
        return UserChatInfo.query.filter(UserChatInfo.global_id == id).first()
    except OperationalError as e:
        logger.info("query_chatbyid errorMsg= {} ".format(e))
        return None


def delete_counterbyid(id):
    """
    根据ID删除Counter实体
    :param id: Counter的ID
    """
    try:
        counter = Counters.query.get(id)
        if counter is None:
            return
        db.session.delete(counter)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_counterbyid errorMsg= {} ".format(e))


def insert_counter(counter):
    """
    插入一个Counter实体
    :param counter: Counters实体
    """
    try:
        db.session.add(counter)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_counter errorMsg= {} ".format(e))


def insert_chat(chat):
    """
    插入一个Chat实体
    :param chat: Chat实体
    """
    try:
        db.session.add(chat)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_chat errorMsg= {} ".format(e))


def update_counterbyid(counter):
    """
    根据ID更新counter的值
    :param counter实体
    """
    try:
        counter = query_counterbyid(counter.id)
        if counter is None:
            return
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_counterbyid errorMsg= {} ".format(e))

def update_chatbyid(chat):
    """
    根据ID更新chat的值
    :param chat实体
    """
    try:
        chat = query_counterbyid(chat.id)
        if chat is None:
            return
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_chatbyid errorMsg= {} ".format(e))
