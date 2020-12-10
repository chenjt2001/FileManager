import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    #app = Flask(__name__, instance_relative_config=True)
    app = Flask('FileExplorer', instance_relative_config=True)
    #app = Flask(__name__.split('.')[0], instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.sqlite'),
    )

    if test_config is None:
        # load the config, if it exists, when not testing
        #app.config.from_object('config')
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    try:
        os.makedirs(app.config['TEMP_PATH'])
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    import db
    db.init_app(app)

    import index, file, auth, gallery
    app.register_blueprint(index.bp)
    app.add_url_rule('/', 'index', index.index)
    app.register_blueprint(file.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(gallery.bp)

    return app

if __name__ == "__main__":
    # To allow aptana to receive errors, set use_debugger=False
    app = create_app()
    app.run()
