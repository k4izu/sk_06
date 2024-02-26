from sk_app.apps import app
from sk_app.sql_functions import DbOp
import sk_app.users_functions as functions
from flask import render_template,Blueprint,request,redirect,session
import mysql.connector


users_login_view=Blueprint('users_login_view',__name__)


# パスの設定
user = "user/"

# ===== 空要素たち =====
# エラーメッセージ
err_msg={}
# 入力データ
login_form={}
signup_form={}
reset_form={}

# ==========================================================
#   ログイン                ("/")
# ==========================================================
@app.route("/login")
def index():
    # 空ボックス
    err_msg={}
    login_form={}
    return render_template(user + "login.html",err_msg=err_msg,login_form=login_form)


# ==========================================================
#   ログイン確認             ("/login/check")
#   OK："/user" NO："login.html"
# ==========================================================
@app.route("/login/check", methods=["POST"])
def login_check():  
    # ===== データ受信
    login_form = request.form
    # ===== 入力項目TBL 
    vtbl = {
        'login_email':"メールアドレス",
        'login_pass':"パスワード"
    }
    # ===== 受信データの空白チェック
    flg = 0
    for key, value in login_form.items():
        #===== 未入力時のエラー処理
        if not value:
            err_msg[key] = vtbl[key] + "が入力されていません"
            flg = 1
        #===== データが送られていない際の処理
        elif login_form[key] == None:
            err_msg[key] = vtbl[key] + "が入力されていません"
            flg = 1
        else:
            #==== エラーメッセージの初期化
            err_msg[key] = ""
    # ===== 入力漏れが合った場合は再び"login.html"へ
    if flg != 0:
        return render_template(user + "login.html",err_msg=err_msg, login_form=login_form)
    else:
        try:
            # === dbからユーザー情報を取得
            dbop=DbOp('users')
            result=dbop.selectAll()
            # reccnt=dbop.selectCnt() # データ件数
            dbop.close()
            flg=0
            for res_data in result:
                # ==== データが含まれているか確認（含まれていればflg=1）
                if (res_data["email"] ==login_form["login_email"]) and (res_data["password"] ==login_form["login_pass"]):
                    flg=1
                    # ===== SESSION保存
                    # session["user_sess"]=res_data["password"] #passwordのみの場合
                    session["user_sess"]=res_data
                    break
            if flg==1:
                err_msg["all"]=""
                # === /userへ
                return redirect('/user') 
            else:
                err_msg["all"]="メールアドレスまたはパスワードが間違っています"
                return render_template(user + "login.html",err_msg=err_msg, login_form=login_form)
        except mysql.connector.errors.ProgrammingError as e:
            print('***DB接続エラー***')        #===pass間違いなど
            print(type(e))  #===例外名出力
            print(e)        #===例外内容出力
        except Exception as e:
            print('***システム運行プログラムエラー***') #===未知のエラー
            print(type(e))  #===例外名出力
            print(e)        #===例外内容出力
        return 


# ==========================================================
#   会員登録                ("/signup")
# ==========================================================
@app.route("/signup", methods=["GET"])
def signup():
    # 空ボックス
    err_msg={}
    signup_form={}
    signup_sess={}
    # === session存在チェック
    if "signup_sess" in session:
        signup_sess=session["signup_sess"]
        # === 必要なデータのみ抽出
        signup_form={
            "signup_name":signup_sess["signup_name"],
            "signup_email":signup_sess["signup_email"],
            "signup_pass":signup_sess["signup_pass"],
        }
    return render_template(user+"signup.html",err_msg=err_msg, signup_form=signup_form)


# ==========================================================
#   会員登録確認             ("/signup/check")
#   OK："/signup/check" NO："signup.html"
# ==========================================================
@app.route("/signup/check", methods=["POST"])
def signup_check():
    # ===== データ受信
    signup_form = request.form
    # ===== 入力項目TBL
    vtbl = {
        'signup_name':"ユーザー名",
        'signup_email':"メールアドレス",
        'signup_pass':"パスワード",
        "signup_pass_check":"パスワード(確認用)"
    }
        # ===== 受信データの空白チェック
    flg = 0
    for key, value in signup_form.items():
        #===== 未入力時のエラー処理
        if not value:
            err_msg[key] = vtbl[key] + "が入力されていません"
            flg = 1
        #===== データが送られていない際の処理
        elif signup_form[key] == None:
            err_msg[key] = vtbl[key] + "が入力されていません"
            flg = 1
        # ===== パスワードが確認用と等しくない場合
        elif signup_form["signup_pass"]!=signup_form["signup_pass_check"]:
            flg=1
            err_msg["all"]="パスワードと確認用が異なります"
            err_msg["signup_pass_check"]="確認用のパスワードが異なります"
        else:
            #==== エラーメッセージの初期化
            err_msg[key] = ""
    # ===== 入力漏れが合った場合は再び"signup.html"へ
    if flg != 0:
        return render_template(user+"signup.html",err_msg=err_msg, signup_form=signup_form)
    session["signup_sess"]=signup_form
    # ===== 登録確認ページ"signup_check.html"へ
    return render_template(user+"signup_check.html",signup_form=signup_form)



# ==========================================================
#   会員登録                    ("/signup/comp")
# ==========================================================
@app.route("/signup/comp", methods=["GET"])
def signup_comp():
    signup_sess={}
    # === session存在チェック
    if "signup_sess" in session:
        signup_sess=session["signup_sess"]
        # === 必要なデータのみ抽出
        signup_form={
            "signup_name":signup_sess["signup_name"],
            "signup_email":signup_sess["signup_email"],
            "signup_pass":signup_sess["signup_pass"],
        }
    else:
        # ===== session確認してなければもう一度signupへ
        return redirect('/signup')
    
    sql1='name,email,password'

    sql2= '"'+signup_form['signup_name']+'",'
    sql2+='"'+signup_form["signup_email"]+'",'
    sql2+='"'+signup_form["signup_pass"]+'"'
    try:
        # ====== 登録処理
        dbop=DbOp('users')
        dbop.insTblWC(sql1,sql2)
        dbop.close()
        # ===== session削除
        session.pop('signup_sess',None)
        # ===== session登録
        session['user_sess']=signup_form
        # ===== checkdel.htmlへ
        return render_template(user+'signup_comp.html')
    except mysql.connector.errors.ProgrammingError as e:
        print('***DB接続エラー***')        #===pass間違いなど
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    except Exception as e:
        print('***システム運行プログラムエラー***') #===未知のエラー
        print(type(e))  #===例外名出力
        print(e)        #===例外内容出力
    




# ==========================================================
#   パスワード再設定              ('/login/reset/password')
# ==========================================================
@app.route("/login/reset/password", methods=["get"])
def reset_password():
    return render_template(user+"reset_password.html",err_msg=err_msg,reset_form=reset_form)


# ==========================================================
#   パスワード再設定完了          ('/login/reset/password/comp')
# ==========================================================
@app.route("/login/reset/password/comp", methods=["get"])
def reset_password_comp():
    return render_template(user+"reset_password_comp.html",err_msg=err_msg,reset_form=reset_form)