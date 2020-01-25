import os
from sanic_script import Manager
from app import create_app

app = create_app('development')
manager = Manager(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, debug=True)
    #manager.run()
