#!/usr/bin/env python

import os
from flask_migrate import Migrate, upgrade
from app import create_app, db

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)

if __name__ == '__main__':
    app.run()
