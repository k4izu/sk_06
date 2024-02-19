from sk_app.apps import app
from flask import render_template,Blueprint,request,redirect

users_model_view=Blueprint('users_model_view',__name__)

# パスの設定
user = "user/"

# ===== 空要素たち =====
# エラーメッセージ
err_msg={}
# 入力データ
model_form={}
signup_form={}

# ==========================================================
#   モデル一覧              ('/model')
# ==========================================================
@app.route("/model")
def model():
    model_data={
        "model_name":"サンプルA",
        "model_img":"画像",
        "model_id":"0000000001"
    }
    return render_template(user+"model.html",model_data=model_data)

# ==========================================================
#   モデル詳細              ('/model/detail')
# ==========================================================
@app.route("/model/detail")
def model_detail():
    return render_template(user+"model_detail.html")


