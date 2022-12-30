from flask import Flask, request ,render_template, redirect  # Flaskは必須、requestはリクエストパラメータを処理する場合に使用します。
from modules.make_Newthread import new_thread, Get_Thread_All, Get_Thread_One, dictionary, Update_Thread_Time, Delete_One_Thread
app = Flask(__name__)

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