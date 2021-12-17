#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2020-11-20 14:42
import os, sys, re, json, traceback, time
from sqlalchemy.ext.declarative import declarative_base
import _locale

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

# 创建对象的基类:
Base = declarative_base()

if __name__ == "__main__":
    pass
