from sk_app.apps import app
from sk_app.sql_functions import DbOp
import sk_app.users_functions as functions
from flask import render_template,Blueprint,redirect
import mysql.connector
# from PIL import Image
from werkzeug.utils import secure_filename
import os
from werkzeug.datastructures import ImmutableDict
from itertools import chain

admin_view=Blueprint('admin_view',__name__,url_prefix='/admin')
users_sql_functions=Blueprint('users_sql_functions',__name__)

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

    sql="select * from users"
    # === 配列格納
    try:
        # ====== モデルデータ抽出
        dbop=DbOp('users')
        user_data=dbop.selectEx(sql)
        dbop.close()
        print(user_data)
        # ===== users_model.htmlへ
        return render_template(admin+'user_data.html',user_data=user_data)
    except mysql.connector.errors.ProgrammingError as e:
        print('***DB接続エラー***')        #===pass間違いなど
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    except Exception as e:
        print('***システム運行プログラムエラー***') #===未知のエラー
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力    

    return render_template(admin + 'user_data.html')

@app.route('/user_devices')
def udevice():
    
    sql="select * from devices"
    # === 配列格納
    try:
        # ====== モデルデータ抽出
        dbop=DbOp('devices')
        devices_data=dbop.selectEx(sql)
        dbop.close()
        print(devices_data)
        # ===== users_model.htmlへ
        return render_template(admin+'user_devices.html',devices_data=devices_data)
    except mysql.connector.errors.ProgrammingError as e:
        print('***DB接続エラー***')        #===pass間違いなど
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    except Exception as e:
        print('***システム運行プログラムエラー***') #===未知のエラー
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力    

    return render_template(admin + 'user_devices.html')
    
    return render_template(admin + 'user_device.html')

class DbOp:
    # ===== コンストラクタ =============
        def __init__(self,table):
            self.__host     ="localhost"
            self.__user     ="root"
            self.__passwd   =""
            self.__db       ="sk_6"
            self.__table    =table

            # DB接続情報
            self.__con=mysql.connector.connect(
                host=self.__host,
                user=self.__user,
                passwd=self.__passwd,
                db=self.__db
            )
        # ===== メソッド ===================
            
        # ===== DB接続 & 全件処理
        def selectAll(self):
            sql='SELECT * FROM ' + self.__table + ';'

            cur=self.__con.cursor(dictionary=True)      #===カーソル作成
            cur.execute(sql)                            #===SQL発行
            res=cur.fetchall()                          #===select結果全件格納
            cur.close()                                 #===カーソルCLOSE

            return res
        
        # ===== DB接続 & 全件抽出ページ指定
        def selectPage(self,pgno,cnt):
            sql='SELECT * FROM ' + self.__table + ';'

            cur=self.__con.cursor(dictionary=True)      #===カーソル作成
            cur.execute(sql)                            #===SQL発行
            tbl=cur.fetchall()                          #===select結果全件格納

            # === 表示ページの指定
            pgno=int(pgno)
            cnt=int(cnt)
            sidx=(pgno-1)*cnt # === ページ指定
            eidx=sidx + cnt # === 個数
            res=tbl[sidx:eidx] # === データをresに

            cur.close()                                 #===カーソルCLOSE
            return res