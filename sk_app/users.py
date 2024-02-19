from sk_app.apps import app
from flask import render_template,Blueprint,request,redirect
import requests

# 分割用
user_view=Blueprint('users_view',__name__,url_prefix='/user')

# ===================================================
# ======    外部モジュール取込
# ===================================================
from sk_app.users_login import users_login_view
#====================================================
# ===== エンドポイント指定  ('/user/login(signup)')
#====================================================
app.register_blueprint(users_login_view)


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
    return render_template(user + "index.html")
