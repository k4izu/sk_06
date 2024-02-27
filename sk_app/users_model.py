from sk_app.apps import app
from sk_app.sql_functions import DbOp
import sk_app.users_functions as functions
from flask import render_template,Blueprint,request,redirect
import mysql.connector

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
    # === sessionが無ければloginページへ
    user_data=functions.session_check()
    if user_data=="FALSE":
        return redirect('/login')
    # === 配列格納
    vtbl={
        "model_img":"画像",
        "model_name":"商品名",
        "model_id":"登録ID"
    }
    # === user_idで登録されているmodelを抽出
    sql=f'user_id = "{user_data["user_id"]}"'
    try:
        # ====== モデルデータ抽出
        dbop=DbOp('models')
        model_data=dbop.selectEx(sql)
        dbop.close()
        print(model_data)
        # ===== users_model.htmlへ
        return render_template(user+'model.html',model_data=model_data,vtbl=vtbl)
    except mysql.connector.errors.ProgrammingError as e:
        print('***DB接続エラー***')        #===pass間違いなど
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    except Exception as e:
        print('***システム運行プログラムエラー***') #===未知のエラー
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力

# ==========================================================
#   モデル詳細              ('/model/detail/<id>')
# ==========================================================
@app.route("/model/detail/<id>",methods=["get"])
def model_detail(id):
    # === sessionが無ければloginページへ
    user_data=functions.session_check()
    if user_data=="FALSE":
        return redirect('/login')
    # === 配列格納
    vtbl={
        "model_img":"画像",
        "model_name":"商品名",
        "model_id":"登録ID"
    }
    # === 選択されたmodelを抽出
    sql=f'id = "{id}"'
    try:
        # ====== モデルデータ抽出
        dbop=DbOp('models')
        model_data=dbop.selectEx(sql)
        dbop.close()
        print(model_data)
        # ===== users_model.htmlへ
        return render_template(user+'model_detail.html',model_data=model_data,vtbl=vtbl)
    except mysql.connector.errors.ProgrammingError as e:
        print('***DB接続エラー***')        #===pass間違いなど
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    except Exception as e:
        print('***システム運行プログラムエラー***') #===未知のエラー
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    test=id
    return render_template(user+"model_detail.html",test=test)


# ==========================================================
#   モデル削除              ('/model/delete/<scode>')
# ==========================================================
@app.route("/model/delete/<id>",methods=["get"])
def model_delete(id):
    test=id
    return render_template(user+"model.html",test=test)


# ==========================================================
#   モデル追加              ('/model/add')
# ==========================================================
@app.route("/model_add",methods=["get"])
def model_add():
    # === sessionが無ければloginページへ
    user_data=functions.session_check()
    if user_data=="FALSE":
        return redirect('/login')
    return render_template(user+'model_add.html',err_msg=err_msg,model_form=model_form)

# ==========================================================
#   モデル追加              ('/model/add/comp')
# ==========================================================
@app.route("/model_add_comp",methods=["post"])
def model_add_comp():
    return render_template(user+'model_add_comp.html')