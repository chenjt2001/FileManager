import os
import time

from flask import current_app


# 时间戳格式化
def timef(timestamp) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

# 文件大小格式化
def sizef(size, precision: int=2) -> str:
    formats = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    unit = 1024.0
    if not(isinstance(size, float) or isinstance(size, int)):
        raise TypeError('a float number or an integer number is required!')
    if size < 0:
        raise ValueError('number must be non-negative')
    for i in formats:
        size /= unit
        if size < unit:
            return f'{round(size, precision)}{i}'
    return f'{round(size, precision)}{i}'

# 规范path字符串形式，默认返回绝对路径
def normpath(path: str, admin: bool=False, rel: bool=False) -> str:
    DATA_DIR = current_app.config['DATA_DIR']

    path = os.path.normpath(path)# 规范化
    # 相对路径转绝对路径
    if not os.path.isabs(path):
        path = '/'.join([DATA_DIR, path])
    path = os.path.normpath(path)# 再次规范化
    path = path.replace('\\', '/')# 统一正斜杠
    # 判断该路径是否属于DATA_DIR
    assert os.path.commonpath([DATA_DIR, path]) == os.path.abspath(DATA_DIR) or admin, '此目录无权访问'# 3.5 Later
    return os.path.relpath(path, DATA_DIR) if rel else path
