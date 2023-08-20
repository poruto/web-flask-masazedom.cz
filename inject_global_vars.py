from flask import *
from __main__ import app

import config

@app.context_processor
def inject_project_name():
    return dict(project_name=config.settings["project_name"])