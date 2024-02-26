from sk_app.apps import app
from sk_app.sql_functions import DbOp
import sk_app.users_functions as functions
from flask import render_template,Blueprint,redirect
import mysql.connector

admin_view=Blueprint('admin_view',__name__,url_prefix='/admin')

# パスの設定
admin = "admin/"

#「/admin」へアクセスがあった場合に、「admin/index.html」へ
@app.route("/admin")
def admin_index():
    return render_template(admin + "index.html")

@app.route('/adminlogin')
def login():
    return render_template(admin + 'login.html')

@app.route('/user_data')
def userdata():

        # === sessionが無ければloginページへ
    # user_data=functions.session_check()
    # if user_data=="FALSE":
    #     return redirect('/login')
    # === 配列格納
    vtbl={
        "model_img":"画像",
        "model_name":"商品名",
        "model_id":"登録ID"
    }

    sql=f'user_id = "{user_data["user_id"]}"'
    try:
        # ====== モデルデータ抽出
        dbop=DbOp('users')
        user_data=dbop.selectEx(sql)
        dbop.close()
        print(user_data)
        # ===== users_model.htmlへ
        return render_template(admin+'user_data.html',user_data=user_data,vtbl=vtbl)
    except mysql.connector.errors.ProgrammingError as e:
        print('***DB接続エラー***')        #===pass間違いなど
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    except Exception as e:
        print('***システム運行プログラムエラー***') #===未知のエラー
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力

    return render_template(admin + 'user_data.html')

@app.route('/userdevices')
def udevice():
    return render_template(admin + 'user_device.html')