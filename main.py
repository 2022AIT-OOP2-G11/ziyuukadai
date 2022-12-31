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


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
       #GETだったら全部のスレッドを取得してindex.htmlに送る
        
        return render_template('index.html', threads=)

    elif request.method == "POST":
        #POSTだったらデータを受け取って、データベースに保存する
        
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)