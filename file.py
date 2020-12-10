import mimetypes
import os

from flask import (Blueprint, current_app, jsonify, redirect,
                   render_template, request, send_file, url_for)

from utils import *
from auth import login_required

bp = Blueprint('file', __name__, url_prefix='/file')

# 获取路径信息
@bp.route('/pathinfo', methods=['GET'])
@login_required
def get_pathinfo():
    abspath = normpath(request.args.get('path'))
    relpath = normpath(request.args.get('path'), rel=True)

    # 文件
    if os.path.isfile(abspath):
        name = os.path.basename(abspath)
        size = os.path.getsize(abspath)
        ctime = os.path.getctime(abspath)
        url = url_for('file.getfile', path=relpath)
        # 判断文件类型
        info = {
            'isfile':True,
            'name':name,
            'size':sizef(size),
            'MIME':mimetypes.guess_type(name, strict=False)[0], #MIME[extension]
            'url':url,
            'ctime':timef(ctime),
        }

    # 文件夹
    else:
        name = (abspath[:-1] if abspath[-1] == '/' else abspath).split('/')[-1]
        ctime = os.path.getctime(abspath)
        info = {
            'isfile':False,
            'name':name,
            'ctime':timef(ctime),
        }

    return jsonify(info)

# 主页面
@bp.route('/')
@login_required
def index():
    return redirect(url_for('file.explorer'))

# 文件浏览
@bp.route('/explorer/', methods=('GET', 'POST'))
@bp.route('/explorer/<path:path>', methods=('GET', 'POST'))
@login_required
def explorer(path=''):
    #print(tuple(g.user))
    if request.method == 'GET':
        abspath = normpath(path)# 绝对路径
        relpath = normpath(path, rel=True)# 相对路径
        if os.path.isfile(abspath):
            path = os.path.dirname(relpath)
        else:
            path = relpath
        return render_template('file/explorer.html', path=path)
    
    else:# POST, 跳转到子目录
        return redirect('/file/explorer/'+request.form['path'])

# 获取文件
@bp.route('/download', methods=['GET'])
@bp.route('/getfile', methods=['GET'])
@login_required
def getfile():
    path = normpath(request.args.get('path'))
    return send_file(path)

'''
# 获取文件十六进制数据
@app.route('/file/gethex', methods=['POST'])
def get_hex():
    path = normpath(request.args.get('path'))
    index = json.load(request.args.get('index').replace('\\','/'))# 一个索引1024字节 从0开始

    if not os.path.isfile(path):
        pass

    with open(path, 'rb') as f:
        f.seek(index*1024)
        f.read()
'''

# 获取文件树json
@bp.route('/filetree', methods=['GET'])
@login_required
def filetree():

    # 制作目录json
    def getDirectoryTree(folder):
        dirtree = {'children':[]}
        if os.path.isfile(folder): 
            return {'text':os.path.basename(folder),'icon':'glyphicon glyphicon-leaf'}
        else:
            basename = os.path.basename(folder)
            dirtree['text'] = basename
            for item in os.listdir(folder):
                dirtree['children'].append(getDirectoryTree(os.path.join(folder,item)))
            return dirtree
    path = normpath(request.args.get('path'))
    return jsonify(list(getDirectoryTree(path).values())[0])# 转换为json再返回
    #with open('path.json' ,'w') as f:
    #    f.write(json.dumps(dir_tree))
