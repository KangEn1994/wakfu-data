#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2020-11-18 14:50
import os, sys, re, json, traceback, time
import _locale

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

from flask import Flask, request, send_file, render_template, redirect, make_response
from flask_restful import Api
from log_obj import logger

app = Flask(__name__, template_folder="template/")


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


api = Api(app)


@api.representation("text/html")
def out_html(data, code, headers=None):
    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    return resp


@app.route('/', methods=['GET'])
def app_html():
    user = request.args.get("user", "")
    if user != "wakfu":
        return "wrong"
    conf_file = open("conf/menu.txt", "r")
    menu_data = conf_file.read().split("\n")
    conf_file.close()
    menu_info = []
    for each in menu_data:
        if not each.startswith("#"):
            each_menu = each.split(",")
            if len(each_menu) == 4:
                menu_info.append(each_menu)
            elif len(each_menu) == 3:
                each_menu.append("show_iframe")
                menu_info.append(each_menu)

    return render_template("index.html", menu_info=menu_info)


@app.route('/static/js/<path:path>', methods=['GET'])
def js_file(path):
    return send_file('template/js/{0}'.format(path))


@app.route('/static/css/<path:path>', methods=['GET'])
def css_file(path):
    return send_file('template/css/{0}'.format(path))


@app.route('/static/img/<path:path>', methods=['GET'])
def img_file(path):
    return send_file('template/img/{0}'.format(path))


@app.route('/static/images/<path:path>', methods=['GET'])
def images_file(path):
    return send_file('template/img/{0}'.format(path))


@app.route('/static/fonts/<path:path>', methods=['GET'])
def fonts_file(path):
    return send_file('template/fonts/{0}'.format(path))


@app.route('/static/md/<path:path>', methods=['GET'])
def md_file(path):
    return send_file('template/idps/markdown/{0}'.format(path))


@app.route('/staticfile/<path:path>', methods=['GET'])
def staticfile(path):
    return send_file('template/{0}'.format(path))


@app.route('/markdown/<path:path>', methods=['GET'])
def markdown_show(path):
    # /markdown/idps/markdown/readme.md
    return render_template('markdown_show.html', markdown_file_path=path)


@app.route('/pdf/<path:filename>', methods=['GET'])
def pdf_file(filename):
    # /markdown/idps/markdown/readme.md
    return send_file('files/{0}'.format(filename))


from tools.utils.template_utils import is_url, is_times
app.add_template_filter(is_url, 'is_url')
app.add_template_filter(is_times, 'is_times')



# 样例
# from  xxxx  import zzzz
#

# 获取token
# from route.control.idps.login_control import LoginToken, LoginUserTransform
# api.add_resource(LoginToken, '/token')
# api.add_resource(LoginUserTransform, '/transform_user')

if __name__ == "__main__":
    # 启动
    app.config['JSON_AS_ASCII'] = False
    app.run(port=9999, host='0.0.0.0')
