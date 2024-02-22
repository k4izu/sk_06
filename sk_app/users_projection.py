from sk_app.apps import app
from flask import render_template,Blueprint,request,redirect

users_projection_view=Blueprint('users_projection_view',__name__)

# パスの設定
user = "user/"

# ===== 空要素たち =====
# エラーメッセージ
err_msg={}
# 入力データ


# ==========================================================
#   投影ホーム              ('/projection')
# ==========================================================
@app.route("/projection")
def projection():
    return render_template(user+"projection.html")