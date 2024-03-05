from sk_app.apps import app
from flask import render_template,Blueprint,request,redirect,session
import mysql.connector
from PIL import Image
from datetime import timedelta

# ====================================================
# ===== sessionチェック    
# ===== 正：userの名前,パスワード 誤："FALSE"
# ====================================================
def session_check():
    user_session={}
    # === session存在チェック、無い場合は/loginへ
    if "user_sess" in session:
        user_session=session["user_sess"]
        # === 必要なデータのみ抽出
        res={
            "user_id":user_session["id"],
            "user_name":user_session["name"],
            "user_email":user_session["email"]
        }
    # === 存在しない場合はログインページへ
    else:
        res="FALSE"
    return res

# 拡張子チェック（img）
def extension_check_img(filename):
    Extencion=['jpg','png','jpeg']
    ex_result = False
    if "." in filename:
        # === 文字列分割で配列化し、拡張子取り出し
        ext = filename.rsplit('.',1)[1]
        # === 小文字に変換
        ext=ext.lower()
        if ext in Extencion:
            # === 許可された演算子ならばTrueで返す
            ex_result = True
    return ex_result

# 拡張子チェック（モデル）
def extension_check_model(filename):
    Extencion=['glb']
    ex_result = False
    if "." in filename:
        # === 文字列分割で配列化し、拡張子取り出し
        ext = filename.rsplit('.',1)[1]
        # === 小文字に変換
        ext=ext.lower()
        if ext in Extencion:
            # === 許可された演算子ならばTrueで返す
            ex_result = True
    return ex_result

# 拡張子チェック（IMG）
def extension_check_img(filename):
    Extencion=['jpg','png']
    ex_result = False
    if "." in filename:
        # === 文字列分割で配列化し、拡張子取り出し
        ext = filename.rsplit('.',1)[1]
        # === 小文字に変換
        ext=ext.lower()
        if ext in Extencion:
            # === 許可された演算子ならばTrueで返す
            ex_result = True
    return ex_result

# ========================================
#   画像をresizeする関数
# ========================================
def img_sizechange(file,maxsize):
    # ===ファイルオープン
    img=Image.open(file)
    # === 画像のリサイズ
    if (img.height >= maxsize) or (img.width >= maxsize):
        if img.height>=img.width:
            height=maxsize
            width=int(img.width*(height/img.height))
        else:
            width=maxsize
            height=int(img.height*(width/img.width))
        newimg=img.resize((width,height))
    else:
        newimg=img.resize((img.width,img.height))
    return newimg