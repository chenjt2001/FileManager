from flask import * # 导入flask模块下的所有元素
import sqlite3 # 导入sqlite3模块

app = Flask('Posts') # 建立Flask应用

DATABASE = 'instance/database.sqlite' # 数据库文件地址
DATABASE_INIT_FILE = 'schema.sql' # 数据库建模文件地址

# init_db()
def init_db(): # 此函数要使用 数据库建模文件 初始化数据库：建立post表（Initial Schemas）。此函数在命令行中使用，仅一次，再次使用会删除数据库中已有数据。
    with app.app_context(): # 官网文档说了原因：不是在Web应用中使用，而是在Python Shell中使用时需要此语句（Connect on Demand）。
        db = get_db()
        with app.open_resource(DATABASE_INIT_FILE, mode='r') as f: # with语句用法！
            db.cursor().executescript(f.read()) # 执行建模文件中的脚本
        db.commit() # 提交事务

# make_dicts()
def make_dicts(cursor, row): # 将查询返回的数据的转换为字典类型，这样会跟方便使用。此函数会在get_db()函数中用到，赋值给db.row_factory。
    return dict((cursor.description[idx][0], value)
                for idx,value in enumerate(row))

# get_db()
def get_db(): # 获取数据库连接
    db = getattr(g, '_database', None) # g对象时一个Flask应用的公共对象（和request、session一样），用于存储用户的数据——整个应用共享！
    if db is None:
        db = g._database = sqlite3.connect(DATABASE) # 建立数据库连接
        db.row_factory = make_dicts # 转换默认的查询数据类型为字典类型，也可以使用sqlite3.Row
    return db # 返回数据库连接，可能返回为None

# close_connection()
@app.teardown_appcontext # 这个装饰器用于实现在请求的最后自动关闭数据库连接的功能
def close_connection(exception): # 关闭数据库连接
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    if input('警告！此程序会删除已存在的数据库并重建！是否继续？(y/n):') == 'y':
        init_db()