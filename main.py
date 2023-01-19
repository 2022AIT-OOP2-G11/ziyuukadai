from flask import Flask, request ,render_template, redirect  # Flaskは必須、requestはリクエストパラメータを処理する場合に使用します。
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import re #正規表現
import json
from modules.thread_operation import new_thread, Get_Thread_All, Get_Thread_One, dictionary, Update_Thread_Time, Delete_One_Thread
from modules.debug_login import new_user, Get_user_All, get_user_by_id, get_user_by_name, dictionary
from modules.comment_operation import connect_db,comment_add,comment_get_id
from modules.user_operation import user_add, get_all_users, get_id_by_user, get_studentnumber_by_user

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["SESSION_COOKIE_SECURE"] = True #Cookieの送信をhttpsに限定

#ログイン機能で必要な設定
app.secret_key = "ahf))ajh>|f<hiwtakoyaki-ehf{haoj!w#g#+=)h"
login_manager = LoginManager()
login_manager.init_app(app)

#セッション有効時間を設定できます(現状デバッグ用に1分)
app.permanent_session_lifetime = timedelta(minutes=.5)

#ログインに必要なユーザクラスを定義
class User(UserMixin):
    def __init__(self, user_name, student_id, id=None):
        self.id = id
        self.user_name = user_name
        self.student_id = student_id

 #セッションからユーザーをリロードするための関数
 #ユーザオブジェクトを返す
@login_manager.user_loader
def load_user(user_id):
    
    # --- ↓DB操作に合わせて、処理を変更する↓ --- #
    #idからユーザデータを取得
    #print("arg_load_user::", user_id)
    get_id_by_user(user_id)
    
    with open('json/Id_by_Users.json', 'r') as f:
            user_json = json.load(f)
    
    user_id = [key for key in user_json.keys()][0]
    user_name = user_json[user_id]["ユーザ名"]
    student_id = user_json[user_id]["学籍番号"]
    
    return User(user_name=user_name, student_id=student_id, id=user_id)
# ==== ⬆︎ここまでログインに必要な設定とか⬆️ ==== #



# ====　⬇︎ここからルーティングおねがいします⬇︎ ==== #

@app.route('/', methods=["GET", "POST"])
#@login_required#←これがついてるページに入るにはログイン必要
def index():
    if request.method == "GET":
    #GETだったら全部のスレッドを取得してindex.htmlに送る
        Get_Thread_All()
        #読み込むファイルパスの指定
        json_file = open("json/All_thread.json",'r')
        json_dict = json.load(json_file)
        #値を格納する場所
        thread_dict_list= []
        #json取り出してdictでまとめる
        for mykey,myvalue in json_dict.items():
            thread_dict_template = {'id': '', 'スレッド名': '', 'ユーザー名': '','スレッドを立てた時間': '','最終更新時間': ''}
            thread_dict_template['id'] = mykey
            thread_dict_template['スレッド名'] = myvalue['スレッド名']
            thread_dict_template['ユーザー名'] = myvalue['ユーザー名']
            thread_dict_template['最終更新時間'] = myvalue['最終更新時間']
            thread_dict_template['スレッドを立てた時間'] = myvalue['スレッドを立てた時間']
            
            #まとめたdictをlistに追加
            thread_dict_list.append(thread_dict_template)
        return render_template('index.html',threads = thread_dict_list)

    elif request.method == "POST":
        #POSTだったらデータを受け取って、データベースに保存する
        user_name = request.form.get("user_name")
        tread_name = request.form.get("title")

        new_thread(tread_name,user_name)
        
        return redirect("/")




## ====== ⬇︎ここからログイン⬇︎ ======= ##

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        #ログイン画面を表示
        return render_template("login.html")
    
    elif  request.method == "POST":
        #送信されたデータからログインを実行
        #フォームの入力を指定する
        student_id = request.form.get("student_id")
        password = request.form.get("password")
        
        # --- ↓DB操作に合わせて、処理を変更する↓ --- #
        #user名前で検索してヒットしたユーザのデータを取得する（←学籍番号で検索に変更する）
        get_studentnumber_by_user(student_number=student_id)
        with open("json/Num_by_Users.json", "r") as f:
            user_json = json.load(f)
        
        #ユーザが見つからなかったときはエラーメッセージを表示
        if len(user_json) == 0:
            message = "学籍番号が違います"
            return render_template("login.html", message=message)
        
        
        user_id = [key for key in user_json.keys()][0]
        user_name = user_json[user_id]["ユーザ名"]
        student_id = user_json[user_id]["学籍番号"]
        password_hash = user_json[user_id]["パスワード"]
        
        #DBから取得したデータからUserオブジェクトを作成
        user = User(user_name=user_name, student_id=student_id, id=user_id)
        
        
        #パスワードのチェック
        if check_password_hash(password_hash, password):
            #あってたらログイン
            login_user(user)
            return redirect("/")
        else:
            #間違ってたらエラーメッセージを表示
            message = "パスワードが違います"
            return render_template("login.html", message=message)


@app.route("/logout")
def logout():
    #ログアウトを実行
    logout_user()
    return redirect("/login")
    
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        #サインアップ画面を表示
        return render_template("signup.html",message=[], completed = [])
    
    elif  request.method == "POST":
        
        #送信されたデータからサインアップを実行
        #フォームの入力を取得
        if request.method == "POST":
            user_name = request.form.get("user_name")
            student_id = request.form.get("student_id")
            # email = request.form.get("email")
            password = request.form.get("password")
        
        #バリデーション　
        message = [] #エラーがあるごとにメッセージを配列に追加していく
        completed = {} #正しく入力されたところは、再入力の必要をなくす
        
        #ユーザ名
        if not user_name: message.append("ユーザ名を入力してください")
        else: completed["user_name"] = user_name
        # if not email: message.append("メールアドレスを入力してください")
        # elif not "@" in email: message.append("メールアドレスが不正です")
        # elif not "." in email: message.append("メールアドレスが不正です")
        # else: completed["email"] = email
        
        #学籍番号
        major =  re. match("\A[evcbmpdsalthkx]{1}", student_id)
        if not student_id: message.append("学籍番号を入力してください")
        else:
            if not major: message.append("正しい学籍番号を入力してください")
            else: 
                regex = "\A" + major.group() + "{1}[0-9]{5}" + major.group() + "{2}\Z"
                if not re.fullmatch(regex, student_id): message.append("正しい学籍番号を入力してください")
                else: completed["student_id"] = student_id
            
        #パスワード
        if not password: message.append("パスワードを入力してください")
        else:
            if re.findall("[^!-~]{1,}", password): message.append("使えない文字があります" + str(re.findall("[^!-~]{1,}", password)))
            if not re.fullmatch("[!-~]{8,32}\Z", password): message.append("8文字以上32文字以下に設定してください")
            if not re.fullmatch("\A(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)[!-~]{0,}\Z", password): message.append("パスワードには大文字、小文字、数字を入れてください")
    
        
        #エラーあり
        if message:
            print(message)
            return render_template("signup.html", message=message, completed=completed)
        #エラーなし
        else:   
            completed["password"] = password
            #パスワードをハッシュ化してDBに保存
            user_add(username=user_name, password=generate_password_hash(password, method="sha256"), student_number=student_id)
            return redirect("/login")
        
        
#ログインしていない状態でログインが必要なページにアクセスしたときの処理
@login_manager.unauthorized_handler
def unauthorized():
    #ログインしていない時の処理 
    return redirect("/login")



# ===== サンプル用 ====== #
@app.route("/sample")
def sample():
   #ログインしていない時の処理 
   #デバッグ用に専用ページに飛ぶ
    elements = [
       {"id":1, "user_name":"takoyaki3", "content":"こんにちは"},
       {"id":2, "user_name":"nikoniko", "content":"おはよう"},
       {"id":3, "user_name":"takashi", "content":"お腹すいた"},
    ]
    return render_template("sample/for文のサンプル.html", elems=elements)

@app.route("/thread" ,methods = ["GET","POST"])
def thread():
    if request.method == "GET":
         thread = request.args.get("thid")
         thread_id = thread[2:]
         #idで書き込み
         comment_get_id(thread_id)
         #json読み込み
         json_file1 = open("json/thread_id_content.json",'r')
         json_dict1 = json.load(json_file1)
         
          #値を格納する場所
         thread_dict_list= []
         #取り出し
         for myvalue in json_dict1:
            thread_dict = {'コメント':''}
            thread_dict['コメント'] = myvalue['内容']
         
            thread_dict_list.append(thread_dict)
         
         return render_template("thread.html",comments = thread_dict_list)
    elif request.method == "POST":
        pass 
        return render_template("thread.html")

if __name__ == '__main__':
    app.run(debug=True)
    
    
    