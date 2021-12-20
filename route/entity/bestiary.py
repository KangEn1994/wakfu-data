#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2021/12/17
import os, sys, re, json, traceback, time
from sqlalchemy import Column, String, Integer, Text, DateTime, Float
from route.entity.base_model import BaseModel




class Bestiary(BaseModel):
    # 表名
    __tablename__ = "bestiary"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }

    # 表结构
    en_name = Column(String(64))    # 怪物名称  英文
    cn_name = Column(String(128))    # 怪物名称  中文
    family_id = Column(Integer)  # 家族id
    min_level = Column(Integer)   # 最低等级
    max_level = Column(Integer)   # 最高等级
    png_path = Column(String(256))    # 图片路径
    catch_boo = Column(String(64))    # 召唤是否可以捕捉
    characteristics = Column(String(256))    # 基础数值属性
    resistances = Column(String(256))    # 攻击防御属性
    spells_ids = Column(String(256))    # 技能的id list
    drop_data = Column(String(256))    # 掉落物数据 id+percent   dict
    trapper_data = Column(String(256))    # 畜牧产物  id+level   dict





if __name__ == "__main__":
    from sqlalchemy import create_engine
    # from route.service.database.sql_pool import SqlPool
    from conf.conf import  MYSQL_PORT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER, MYSQL_DATABASE


    engine = create_engine(
        'mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.format(
            MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE))
    # engine = create_engine(
    #     'mysql+mysqlconnector://xxxxx:3306/xxxx')
    # 创建DBSession类型:
    # DBSession = sessionmaker(bind=engine)
    # session1 = DBSession()
    Base.metadata.create_all(engine)