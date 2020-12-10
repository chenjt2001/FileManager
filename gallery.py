import mimetypes
import os
import re
import tempfile
import time

import exifread
from flask import (Blueprint, current_app, jsonify, render_template, request,
                   send_file, url_for)
from PIL import Image

from auth import login_required
from utils import *

bp = Blueprint('gallery', __name__, url_prefix='/gallery')

'''
photos = [
    {
        'date': '2020-01-01',
        'images': [
            {
                'id': 0,
                'original': 'http://...',
                'thumbnail': 'http://...',
            },
            {
                'id': 1,
                'original': 'http://...',
                ...,
            }
        ],
    },
    {
        'date': '...'
        'images': [...]
    }
]

'''

# 主页面
@bp.route('/')
@login_required
def index():
    return render_template('gallery/index.html')
    
# 获取缩略图
@bp.route('/thumbnail', methods=['GET'])
@login_required
def get_thumbnail():
    tempfile.tempdir = current_app.config['TEMP_PATH']
    path = normpath(request.args.get('path'))
    im = Image.open(path)
    im.thumbnail((300,100))# max size
    with tempfile.NamedTemporaryFile(delete=False) as f:
        im.save(f, 'JPEG')
    return send_file(f.name, mimetype='image/jpeg')

# 获取photo列表
@bp.route('/list', methods=['GET'])
@login_required
def get_list():

    photos = []
    for root, dirs, files in os.walk(current_app.config['PHOTO_DIR']):
        for name in files:
            path = os.path.join(root, name)
            #print(path)

            if mimetypes.guess_type(name, strict=False)[0] == "image/jpeg":
                image_item = {}
                image_item['thumbnail'] = url_for('gallery.get_thumbnail', path=path)
                image_item['original'] = url_for('file.getfile', path=path)

                # 读取照片拍摄日期
                with open(path, 'rb') as f:
                    tags = exifread.process_file(f)
                    for tag, value in tags.items():
                        if re.match('Image DateTime', tag):
                            image_item['date'] = str(value).replace(':', '').replace(' ','')[:8]
                if 'date' not in image_item.keys():
                    image_item['date'] = time.strftime("%Y%m%d", time.localtime(os.path.getmtime(path)))

                # 如果该照片日期不在photos中则加入
                date_set = set()
                for i, date_item in enumerate(photos):
                    date_set.add(date_item['date'])
                    if date_item['date'] == image_item['date']:
                        index = i
                if image_item['date'] not in date_set:
                    photos.append({
                        'date': image_item['date'],
                        'images': [],
                    })
                    index = -1
                
                # 将image_item加入photos
                photos[index]['images'].append(image_item)
    
    return jsonify(photos)
