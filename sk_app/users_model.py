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
@app.route("/model",methods=["get"])
def model():
    model_data=[
        {"model_name":"サンプルA",
        "model_img":"画像",
        "model_id":"0000000001"},
        {"model_name":"サンプルB",
        "model_img":"画像",
        "model_id":"0000000002"}
    ]
    vtbl={
        "model_img":"画像",
        "model_name":"商品名",
        "model_id":"登録ID"
    }
    return render_template(user+"model.html",model_data=model_data,vtbl=vtbl)

# ==========================================================
#   モデル詳細              ('/model/detail/<scode>')
# ==========================================================
@app.route("/model/detail/<scode>",methods=["get"])
def model_detail(scode):
    test=scode
    return render_template(user+"model_detail.html",test=test)


# ==========================================================
#   モデル削除              ('/model/delete/<scode>')
# ==========================================================
@app.route("/model/delete/<scode>",methods=["get"])
def model_delete(scode):
    test=scode
    return render_template(user+"model.html",test=test)