#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2020-11-13 16:11
import os, sys, re, json, traceback, time
import _locale

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])


def get_length(result):
    return len(result)


def length_is_zero(result):
    return len(result) == 0

def is_url(result):
    if re.search('htt[ps]{1,2}://', str(result)):
        return True
    else:
        return False

def is_times(result):
    """是否是x次的形式"""
    if re.search('\d次', str(result)):
        return True
    else:
        return False


if __name__ == "__main__":
    pass
