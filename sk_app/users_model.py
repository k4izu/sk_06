from sk_app.apps import app
from sk_app.sql_functions import DbOp
import sk_app.users_functions as functions
from flask import render_template,Blueprint,request,redirect,session
import mysql.connector
from datetime import datetime
from werkzeug.utils import secure_filename
import os

users_model_view=Blueprint('users_model_view',__name__)
app.config['MAX_CONTENT_LENGTH']=2*1024*1024

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
    sql=f'user_id = "{user_data["user_id"]}" AND deleted_at IS NULL'
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


# ==========================================================
#   モデル削除              ('/model/delete/<scode>')
# ==========================================================
@app.route("/model/delete/<id>",methods=["get"])
def model_delete(id):
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
        # ===== users_model.htmlへ
        return render_template(user+'model_delete.html',model_data=model_data,vtbl=vtbl)
    except mysql.connector.errors.ProgrammingError as e:
        print('***DB接続エラー***')        #===pass間違いなど
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    except Exception as e:
        print('***システム運行プログラムエラー***') #===未知のエラー
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力


# ==========================================================
#   モデル削除              ('/model/delete/comp/<id>')
# ==========================================================
@app.route("/model/delete/comp/<id>",methods=["get"])
def model_delete_comp(id):
    # === sessionが無ければloginページへ
    user_data=functions.session_check()
    if user_data=="FALSE":
        return redirect('/login')
    
    # 現在の時刻を削除日へ
    sql1='deleted_at=NOW()'
    sql2 ='id='+str(id)
    print(sql1,sql2)
    try:
        # ====== 削除処理
        dbop=DbOp('models')
        dbop.updTbl(sql1,sql2)
        dbop.close()
        return redirect('/model')
    except mysql.connector.errors.ProgrammingError as e:
        print('***DB接続エラー***')        #===pass間違いなど
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    except Exception as e:
        print('***システム運行プログラムエラー***') #===未知のエラー
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力

# ==========================================================
#   モデル追加              ('/model/add')
# ==========================================================
@app.route("/model/add",methods=["get"])
def model_add():
    # === sessionが無ければloginページへ
    user_data=functions.session_check()
    if user_data=="FALSE":
        return redirect('/login')
    return render_template(user+'model_add.html',err_msg=err_msg,model_form=model_form)

# ==========================================================
#   モデル追加              ('/model/add/comp')
# ==========================================================
@app.route("/model/add/comp",methods=["post"])
def model_add_comp():
    # === sessionが無ければloginページへ
    user_data=functions.session_check()
    if user_data=="FALSE":
        return redirect('/login')

    err_msg={}  
    # ===== データ受信
    model_form=request.form
    # ===== 入力項目TBL 
    vtbl = {
        'model_name':"名前",
        'model_info':"モデル情報",
        'model_file_name':"モデルデータ",
        'model_image':"モデル画像",
    }
    # ===== 受信データの空白チェック
    flg = 0
    for key, value in model_form.items():
        #===== 未入力時のエラー処理
        if not value:
            err_msg[key] = vtbl[key] + "が入力されていません"
            flg = 1
        #===== データが送られていない際の処理
        elif model_form[key] == None:
            err_msg[key] = vtbl[key] + "が入力されていません"
            flg = 1
        else:
            #==== エラーメッセージの初期化
            err_msg[key] = ""
    # ===ファイル受信
    data_file=request.files['model_file_name']
    img_file=request.files['model_image']
    # ===ローカルファイル名取得
    filenameMF=data_file.filename
    filenameMI=img_file.filename
    # ===ファイル未受信の場合はmodel.htmlへ
    if not filenameMF:
        flg = 1
        err_msg["model_file_name"]="モデルデータが入力されていません"
    if not filenameMI:
        flg = 1
        err_msg["model_image"]="モデル画像が選択されていません"
    # ===== 入力漏れが合った場合は再び"model_add.html"へ
    if flg != 0:
        return render_template(user + "model_add.html",err_msg=err_msg, model_form=model_form)
    
    # ===日付情報取得
    savedate=datetime.now().strftime("%Y%m%d_%H%M%S_")
    for key in request.files:
       files = request.files.getlist(key)
       for file in files:
           if file.filename == '':
               continue
           if key == 'model_image':
                # ===== 画像のリサイズ
                maxsize=500
                img01=functions.img_sizechange(img_file,maxsize)
                # ===日付情報を混ぜたものを画像ファイル名に
                imagefile=savedate+secure_filename(filenameMI)
                # ===保存用フルパス作成（画像）
                save_path1=os.path.join('./sk_app/static/uploads/img/',imagefile)
                img01.save(save_path1,quality=90)
           else:
                # ===日付情報を混ぜたものをデータファイル名に
                modelfile=savedate+secure_filename(filenameMF)
                # ===保存用フルパス作成（画像）
                save_path2=os.path.join('./sk_app/static/uploads/models/',modelfile)
                data_file.save(save_path2)

    sql1='user_id,name,model_file_name,model_image,model_info'
    
    sql2= ''+str(user_data['user_id'])+','
    sql2+= '"'+model_form['model_name']+'",'
    sql2+='"'+modelfile+'",'
    sql2+='"'+imagefile+'",'
    sql2+='"'+model_form["model_info"]+'"'
    try:
        # ====== 登録処理
        dbop=DbOp('models')
        dbop.insTblWC(sql1,sql2)
        dbop.close()
        return redirect('/model')
    except mysql.connector.errors.ProgrammingError as e:
        print('***DB接続エラー***')        #===pass間違いなど
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    except Exception as e:
        print('***システム運行プログラムエラー***') #===未知のエラー
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    print(sql1,sql2)
    return render_template(user+'model_add_comp.html')