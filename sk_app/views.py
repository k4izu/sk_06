from sk_app.apps import app
from flask import render_template

# ===================================================
# ======    外部モジュール取込
# ===================================================
from sk_app.users import user_view
from sk_app.admin import admin_view
from sk_app.test import test_view

#====================================================
# ===== エンドポイント指定  ('/user')
#====================================================
app.register_blueprint(user_view)
#====================================================
# ===== エンドポイント指定  ('/admin')
#====================================================
app.register_blueprint(admin_view)
#====================================================
# ===== エンドポイント指定  ('/test')
#====================================================
app.register_blueprint(test_view)

