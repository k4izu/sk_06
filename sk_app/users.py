from sk_app.apps import app
import sk_app.users_functions as functions
from flask import render_template,Blueprint,request,redirect,session
import mysql.connector
from datetime import timedelta

# 分割用
user_view=Blueprint('users_view',__name__,url_prefix='/user')

# ===== SESSION用初期設定
app.secret_key='ryuuzoji'
app.permanent_session_lifetime=timedelta(minutes=150)

# ===================================================
# ======    外部モジュール取込
# ===================================================
from sk_app.users_login import users_login_view
from sk_app.users_model import users_model_view
from sk_app.users_projection import users_projection_view
from sk_app.users_settings import users_settings_view
from sk_app.users_manual import users_manual_view
# from sk_app.users_functions import users_functions

# ===================================================
# ======    エンドポイント指定
# ===================================================
# ===== ('/user/login(signup)')
app.register_blueprint(users_login_view)
# ===== ('/user/model')
app.register_blueprint(users_model_view)
# ===== ('/user/projection')
app.register_blueprint(users_projection_view)
# ===== ('/user/settings')
app.register_blueprint(users_settings_view)
# ===== ('/user/manual')
app.register_blueprint(users_manual_view)
# ===== (usersの関数)
# app.register_blueprint(users_functions)


from sk_app.sql_functions import DbOp

# パスの設定
user = "user/"
# ===== 空要素たち =====
# エラーメッセージ
err_msg={}

# ==========================================================
#   会員のホーム             ("/")
#   ※ログイン後表示
# ==========================================================
@app.route("/")
def user_index():
    # === sessionが無ければloginページへ
    user_data=functions.session_check()
    if user_data=="FALSE":
        return redirect('/login')
    return render_template(user + "index.html",user_data=user_data)
