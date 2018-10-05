#!/usr/bin/env python3

from flask import Flask

app = Flask( __name__ )


from ShopApp.admin.routes import *
from ShopApp.routes import *
from ShopApp.dashboard import *

app.register_blueprint( mod )
app.register_blueprint( admin.routes.mod, url_prefix='/admin' )
