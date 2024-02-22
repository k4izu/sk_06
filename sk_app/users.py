from sk_app.apps import app
from flask import render_template,Blueprint,request,redirect,session
import mysql.connector
from datetime import timedelta

# 分割用
user_view=Blueprint('users_view',__name__,url_prefix='/user')

# ===== SESSION用初期設定
app.secret_key='ryuuzoji'
app.permanent_session_lifetime=timedelta(minutes=3)

# ===================================================
# ======    外部モジュール取込
# ===================================================
from sk_app.users_login import users_login_view
from sk_app.users_model import users_model_view
from sk_app.users_projection import users_projection_view
from sk_app.users_settings import users_settings_view
from sk_app.users_manual import users_manual_view

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


from sk_app.sql_functions import DbOp

# パスの設定
user = "user/"
# ===== 空要素たち =====
# エラーメッセージ
err_msg={}

# ==========================================================
#   会員のホーム             ("/user")
#   ※ログイン後表示
# ==========================================================
@app.route("/user")
def user_index():
    user_session={}
    # === session存在チェック、無い場合は/loginへ
    if "user_sess" in session:
        user_session=session["user_sess"]
    else:
        # === 存在しない場合はログインページへ
        return redirect('/')
    # print(user_session)
    # === 必要なデータのみ抽出
    user_data={
        "user_name":user_session["name"],
        "user_email":user_session["email"]
    }
    print(user_data)
    return render_template(user + "index.html",user_data=user_data)
