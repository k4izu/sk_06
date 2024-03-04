from sk_app.apps import app
from sk_app.sql_functions import DbOp
import sk_app.users_functions as functions
from flask import render_template,Blueprint,request,redirect,jsonify,session
import mysql.connector
from flask_cors import CORS


CORS(app)

users_projection_view=Blueprint('users_projection_view',__name__)

# パスの設定
user = "user/"

# ===== 空要素たち =====
# エラーメッセージ
err_msg={}
# 入力データ
vtbl={}

# ==========================================================
#   投影ホーム              ('/projection')
# ==========================================================
@app.route("/projection")
def projection():
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
    sql=f'user_id = "{user_data["user_id"]}" AND deleted_at IS NULL'
    try:
        # ====== モデルデータ抽出
        dbop=DbOp('models')
        model_data=dbop.selectEx(sql)
        dbop.close()
        print(model_data)
        # ===== users_model.htmlへ
        return render_template(user+'projection.html',model_data=model_data,vtbl=vtbl)
    except mysql.connector.errors.ProgrammingError as e:
        print('***DB接続エラー***')        #===pass間違いなど
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    except Exception as e:
        print('***システム運行プログラムエラー***') #===未知のエラー
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    return render_template(user+"projection.html")

# ==========================================================
#   投影ホーム              ('/projection/<id>')
# ==========================================================
@app.route("/projection/<id>",methods=["get"])
def projection_id(id):
    # return render_template(user+'projection_model.html')
    # === sessionが無ければloginページへ
    user_data=functions.session_check()
    if user_data=="FALSE":
        return redirect('/login')
    print(user_data["user_id"])
    print(id)
    # === user_idで登録されているmodelを抽出
    sql=f'user_id = "{user_data["user_id"]}" AND id = "{id}"'
    try:
        # ====== モデルデータ抽出
        dbop=DbOp('models')
        model_data=dbop.selectEx(sql)
        dbop.close()
        print(model_data)
        session["projection_model"]=model_data[0]["model_file_name"]
        # ===== projection.htmlへ
        return render_template(user+'projection_model.html',model_data=model_data,vtbl=vtbl)
    except mysql.connector.errors.ProgrammingError as e:
        print('***DB接続エラー***')        #===pass間違いなど
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    except Exception as e:
        print('***システム運行プログラムエラー***') #===未知のエラー
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力


# データ引き渡し用
@app.route('/model_data')
def model_data():
    data=session["projection_model"]
    print(data)
    return jsonify(data)

# データ引き渡し用
@app.route('/mediapipe_data')
def mediapipe_data():
    # データを作成
    data = {
        'key1': 'OK',
        'key2': 'value2'
    }
    return jsonify(data)

# === 退避
@app.route("/break/page",methods=["get"])
def break_page():
    return render_template('test02.html')
