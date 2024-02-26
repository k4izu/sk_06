from sk_app.apps import app
from sk_app.sql_functions import DbOp
import sk_app.users_functions as functions
from flask import render_template,Blueprint,request,redirect

users_settings_view=Blueprint('users_settings_view',__name__)

# パスの設定
user = "user/"

# ===== 空要素たち =====
# エラーメッセージ
err_msg={}
# 入力データ


# ==========================================================
#   投影ホーム              ('/settings')
# ==========================================================
@app.route("/settings")
def settings():
    return render_template(user+"settings.html")