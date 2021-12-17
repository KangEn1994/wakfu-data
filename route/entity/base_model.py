#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2021/12/17
import os, sys, re, json, traceback, time
from sqlalchemy import Column, String, Integer, Text, DateTime, Float
from route.entity.base import Base

class BaseModel(Base):
    id = Column(Integer(), primary_key=True)  # id
    remarks = Column(String(256))  # 备注
    delete_flag = Column(Integer())  # 删除标记
    create_by = Column(Integer())   # 创建者
    create_time = Column(DateTime())  # 创建时间
    update_by = Column(Integer())   # 修改者
    update_time = Column(DateTime())  # 修改时间



if __name__ == "__main__":
    pass
