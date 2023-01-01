from flask import Flask, request ,render_template, redirect  # Flaskは必須、requestはリクエストパラメータを処理する場合に使用します。
from flask_login import LoginManager, UserMixin, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import re #正規表現
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
        self.user_name = user_name
    #メモ::get_id()のオーバーライドが必要かも←調べる

#セッションからユーザーをリロードするのに必要っぽい        
@login_manager.user_loader
#get_id()を書いたらここの引数にget_id()を指定する
def load_user(user_id):
    return User.query.get(int(user_id))

#牧村用リンク
#user class:  https://flask-login.readthedocs.io/en/latest/#Your%20User%20Class
#user_login: https://flask-login.readthedocs.io/en/latest/#flask_login.LoginManager.user_loader



@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
       #GETだったら全部のスレッドを取得してindex.htmlに送る
        
        return render_template('index.html')#←デバッグ用
        #return render_template('index.html', threads=)

    elif request.method == "POST":
        #POSTだったらデータを受け取って、データベースに保存する
        
        return redirect("/")




## ====== ⬇︎ここからログイン⬇︎ ======= ##

@app.route("/test_login")
@login_required
def test_login():
    return render_template("test_login/test.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        #ログイン画面を表示
        return render_template("test_login/login.html")
        pass
    
    elif  request.method == "POST":
        #送信されたデータからログインを実行
        pass

@app.route("/logout")
def logout():
    #ログアウトを実行
    pass
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        #サインアップ画面を表示
        return render_template("test_login/signup.html", completed = [])
    
    elif  request.method == "POST":
        
        #送信されたデータからサインアップを実行
        if request.method == "POST":
            user_name = request.form.get("user_name")
            email = request.form.get("email")
            password = request.form.get("password")
        
        print(not user_name)
        #バリデーション
        message = []
        completed = {}
        if not user_name: message.append("ユーザ名を入力してください")
        else: completed["user_name"] = user_name
        if not email: message.append("メールアドレスを入力してください")
        elif not "@" in email: message.append("メールアドレスが不正です")
        elif not "." in email: message.append("メールアドレスが不正です")
        else: completed["email"] = email
        if not password: message.append("パスワードを入力してください")
        elif re.findall("[^!-~]{1,}", password): print("使えない文字があります", re.findall("[^!-~]{1,}", password))
        elif not re.fullmatch("\A(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)[!-~]{8,100}\Z", password): message.append("パスワードは大文字、小文字、数字を含んだ8文字以上100文字以下に設定してください")
        else: completed["password"] = password
        
        #エラーあり
        if message:
            print(message)
            return render_template("signup.html", message=message, completed=completed)
        #エラーなし
        else:   
            #パスワードをハッシュ化してDBに保存
            user = User(user_name=user_name, password=generate_password_hash(password, method="sha256"))
            
            #DBに追加
            
            return redirect("/login")
        
        
        

#ログインしていない状態でログインが必要なページにアクセスしたときの処理
@login_manager.unauthorized_handler
def unauthorized():
    #ログインしていない時の処理 
    return render_template("test_login/unauthorized.html")



if __name__ == '__main__':
    app.run(debug=True)
    
    
    