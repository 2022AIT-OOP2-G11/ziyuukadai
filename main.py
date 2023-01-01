from flask import Flask, request ,render_template, redirect  # Flaskは必須、requestはリクエストパラメータを処理する場合に使用します。
from flask_login import LoginManager, UserMixin, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from modules.make_Newthread import new_thread, Get_Thread_All, Get_Thread_One, dictionary, Update_Thread_Time, Delete_One_Thread

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False 
app.config["SESSION_COOKIE_SECURE"] = True #Cookieの送信をhttpsに限定

#ログイン機能で必要な設定
app.secret_key = "ahf))ajh>|f<hiwehf{haoj!w#g#+=)h"
login_manager = LoginManager()
login_manager.init_app(app)

#セッション有効時間を設定できます(現状デバッグ用に1分)
app.permanent_session_lifetime = timedelta(minutes=1)

#ログインに必要なユーザクラスを定義
class User(UserMixin):
    def __init__(self, id, user_name):
        self.id = id
        self.urew_name = user_name
    #メモ::get_id()のオーバーライドが必要かも←調べる

#セッションからユーザーをリロードするのに必要っぽい        
@login_manager.user_loader
#get_id()を書いたらここの引数にget_id()を指定する
def load_user(user_id):
    return User.query.get(int(user_id))

#牧村用リンク
#user class:  https://flask-login.readthedocs.io/en/latest/#Your%20User%20Class
#user_login: https://flask-login.readthedocs.io/en/latest/#flask_login.LoginManager.user_loader


# ==== ⬆︎ここまでログインに必要な設定とか⬆️ ==== #

# ====　⬇︎ここからルーティングおねがいします⬇︎ ==== #

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
       #GETだったら全部のスレッドを取得してindex.htmlに送る
        
        return render_template('index.html', threads=)

    elif request.method == "POST":
        #POSTだったらデータを受け取って、データベースに保存する
        
        return redirect("/")




## ====== ⬇︎ここからログイン⬇︎ ======= ##

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        #ログイン画面を表示
        pass
    elif  request.method == "POST":
        #送信されたデータからログインを実行
        pass

@app.route("/logout")
def logout():
    #ログアウト画面を表示
    pass
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        #サインアップ画面を表示
        pass
    elif  request.method == "POST":
        #送信されたデータからサインアップを実行
        pass




if __name__ == '__main__':
    app.run(debug=True)
    
    
    