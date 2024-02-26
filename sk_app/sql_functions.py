from sk_app.apps import app
from flask import Flask,render_template,request,session,redirect,make_response,url_for,Blueprint
from datetime import timedelta, datetime
import mysql.connector
# from PIL import Image
from werkzeug.utils import secure_filename
import os
from werkzeug.datastructures import ImmutableDict
from itertools import chain


users_sql_functions=Blueprint('users_sql_functions',__name__)


# ====================================================
# ===== PY24DB操作クラス
# ====================================================
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



# ======================================================================
# ========                  ここより下は関数です
# ======================================================================
# ========================================
#   errorhandlerによるエラーハンドリング
# ========================================
@app.errorhandler(413)
def err404(err):
    err = {
        "code":"413",
        "msg":"画像ファイルを2MB以下にしてください"
    }
    return render_template('error.html',err=err),413

@app.errorhandler(404)
def err404(err):
    err = {
        "code":"404",
        "msg":"ページが見つかりません"
    }
    return render_template('error.html',err=err),404

@app.errorhandler(500)
def err500(err):
    err = {
        "code":"500",
        "msg":"内部サーバーエラー"
    }
    return render_template('error.html',err=err),500