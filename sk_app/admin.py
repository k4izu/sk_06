from sk_app.apps import app
from sk_app.sql_functions import DbOp
import sk_app.users_functions as functions
from flask import render_template,Blueprint,redirect,request
import mysql.connector

admin_view=Blueprint('admin_view',__name__,url_prefix='/admin')
users_sql_functions=Blueprint('users_sql_functions',__name__)

# パスの設定
admin = "admin/"

# 管理者ログイン画面
@app.route('/adminlogin')
def login():

    login = {}
    
    return render_template(admin + 'login.html',login=login)


#「/admin」へアクセスがあった場合に、「admin/index.html」へ
@app.route("/admin")
def admin_index():

    # id = request.form["id"]
    # password = request.form["password"]
    
    # sql = "SELECT id , password FROM admins WHERE'" + id + "'and'" + password + "';"
    
    # try:
    # # ====== モデルデータ抽出
    #     dbop=DbOp('admins')
    #     result=dbop.selectEx(sql)
    #     dbop.close()
    #     print(result)
    # except mysql.connector.errors.ProgrammingError as e:
    #     print('***DB接続エラー***')        #===pass間違いなど
    #     print(type(e))  #===例外名出力
    #     print(e)        #===例外内容出力
    # except Exception as e:
    #     print('***システム運行プログラムエラー***') #===未知のエラー
    #     print(type(e))  #===例外名出力
    #     print(e)        #===例外内容出力 


    # 受信したメール件数表示するための配列格納
    reccnt={}

    try:
    # ====== モデルデータ抽出
        dbop=DbOp('inquiries')
        reccnt=dbop.selectCnt()
        dbop.close()
        print(reccnt)
    except mysql.connector.errors.ProgrammingError as e:
        print('***DB接続エラー***')        #===pass間違いなど
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    except Exception as e:
        print('***システム運行プログラムエラー***') #===未知のエラー
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力 

    return render_template(admin + "index.html",reccnt=reccnt)

# userdata（IDやパスワードなど）の全件抽出
@app.route('/user_data')
def userdata():

    # === 配列格納
    user_data={}
    try:
        # ====== モデルデータ抽出
        dbop=DbOp('users')
        user_data=dbop.selectAll()
        dbop.close()
        # print(user_data)
        # ===== users_model.htmlへ
        # return render_template(admin+'user_data.html',user_data=user_data)
    except mysql.connector.errors.ProgrammingError as e:
        print('***DB接続エラー***')        #===pass間違いなど
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    except Exception as e:
        print('***システム運行プログラムエラー***') #===未知のエラー
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力    

    return render_template(admin + 'user_data.html',user_data=user_data)


# userの使用デバイス全件抽出
@app.route('/user_devices')
def user_devices():
    
    # === 配列格納
    devices_data={}
    try:
        # ====== モデルデータ抽出
        dbop=DbOp('devices')
        devices_data=dbop.selectAll()
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

@app.route("/mail")
def mail():

    # 受信したメール件数表示するための配列格納
    reccnt={}

    try:
    # ====== モデルデータ抽出
        dbop=DbOp('inquiries')
        result=dbop.selectAll()
        reccnt=dbop.selectCnt()
        dbop.close()
        print(reccnt)
    except mysql.connector.errors.ProgrammingError as e:
        print('***DB接続エラー***')        #===pass間違いなど
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    except Exception as e:
        print('***システム運行プログラムエラー***') #===未知のエラー
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力 

    return render_template(admin + "mail.html",reccnt=reccnt,result=result)


# データベース接続関係
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
    # ===== DB接続 & 絞り込み条件抽出
        def selectEx(self,ex):
            sql='SELECT * FROM ' + self.__table + ' WHERE ' + ex + ';'

            cur=self.__con.cursor(dictionary=True)      #===カーソル作成
            cur.execute(sql)                            #===SQL発行
            res=cur.fetchall()                          #===select結果全件格納
            cur.close()                                 #===カーソルCLOSE

            # === 二次元配列を返す
            return res
        
        # ===== DB接続 & 絞り込み条件抽出（1件のみ）
        def selectOne(self,ex):
            sql='SELECT * FROM ' + self.__table + ' WHERE ' + ex + ';'

            cur=self.__con.cursor(dictionary=True)      #===カーソル作成
            cur.execute(sql)                            #===SQL発行
            res=cur.fetchall()                          #===select結果全件格納
            cur.close()                                 #===カーソルCLOSE

            # === 二次元配列の0行目（一件）のみを返す
            return res[0]
        
        # ===== DB接続 & データ件数取得
        def selectCnt(self):
            sql='SELECT COUNT(*) AS reccnt FROM ' + self.__table + ';'

            cur=self.__con.cursor(dictionary=True)      #===カーソル作成
            cur.execute(sql)                            #===SQL発行
            res=cur.fetchall()                          #===select結果全件格納
            cur.close()                                 #===カーソルCLOSE

            # === 二次元配列の0行目（一件）のみを返す　※件数
            return res[0]
        
        # ===== DB接続 & データ挿入
        def insTbl(self,val):
            sql ='INSERT INTO ' + self.__table + ' VALUES('
            sql+=val
            sql+=');'

            cur=self.__con.cursor(dictionary=True)      #===カーソル作成
            cur.execute(sql)                            #===SQL発行
            self.__con.commit()                         #===commit
            cur.close()                                 #===カーソルCLOSE


        # ===== DB接続 & データ挿入（数個だけ）
        def insTblWC(self,val1,val2):
            sql ='INSERT INTO ' + self.__table + '(' + val1 + ') VALUES('
            sql+=val2
            sql+=');'

            cur=self.__con.cursor(dictionary=True)      #===カーソル作成
            cur.execute(sql)                            #===SQL発行
            self.__con.commit()                         #===commit
            cur.close()    

        # ===== DB接続 & データ変更
        def updTbl(self,val1,val2):
            sql ='UPDATE ' + self.__table + ' SET ' + val1 + 'WHERE'
            sql+=val2
            sql+=';'

            cur=self.__con.cursor(dictionary=True)      #===カーソル作成
            cur.execute(sql)                            #===SQL発行
            self.__con.commit()                         #===commit
            cur.close()    


        # ===== DB接続 & データ削除
        def delTbl(self,val):
            sql ='DELETE FROM ' + self.__table + ' WHERE '
            sql+=val
            sql+=';'

            cur=self.__con.cursor(dictionary=True)      #===カーソル作成
            cur.execute(sql)                            #===SQL発行
            self.__con.commit()                         #===commit
            cur.close()                                 #===カーソルCLOSE

        # ===== DB切断
        def close(self):
            self.__con.close()                      #===DB CLOSE