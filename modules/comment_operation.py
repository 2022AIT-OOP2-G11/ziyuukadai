import sqlite3
import json

# id	スレッドid	内容	ユーザー名	 投稿時間
# 1, 2,  int	 string	   string	YY:MM:DD:mm:ss　　

# connect_db -> スレッドに接続する。もし、テーブルがなければテーブルを作成(引数なし)
# comment_add -> コメントを追加(引数 : スレッドid, 内容, ユーザー名)
# comment_get_id -> スレッドidに応じたスレッドの内容をjsonファイルへ保存(引数 : thread_id)

content_db = './DB/DataBase.db' #DBの保存場所

#指定されたスレッドのDBに接続し、テーブルが作成されていない場合作成
def connect_db():
    con = sqlite3.connect(content_db) #DBに接続

    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0]

    #テーブルが作成されていない場合は作成
    if table_count == 0:
        con.execute("CREATE TABLE コメント(id INTEGER PRIMARY KEY AUTOINCREMENT, スレッドid INTEGER NOT NULL, 内容 TEXT NOT NULL, ユーザー名 TEXT, 投稿時間 TIMESTAMP)")

#コメントを追加 → (スレッドid, 内容, ユーザー名)
def comment_add(thread_id, content, user_name, student_num): 
     # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/DataBase.db')

    #テーブル(表)があるか確認
    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='コメント'").fetchone()[0]
    # print(table_count) #デバック

    if table_count == 0: #なかったらテーブルを作成して追加
        
        #テーブル作成SQL文
        con.execute("CREATE TABLE コメント(id INTEGER PRIMARY KEY, スレッドid INTEGER NOT NULL" +
                        ", 内容 TEXT NOT NULL, ユーザー名 STRING NOT NULL, 学籍番号 STRING NOT NULL, '投稿時間' TIMESTAMP)")

        #新規作成した時スレッドIDが0のため1を代入
        count = 1

    else: #あったらコメントの個数を取得して追加する
        #コメントの数を確認
        thread_count = con.execute("SELECT count(id) FROM コメント")
        count = int(thread_count.fetchone()[0])

        #一番高いスレッドIDを作成
        count += 1
        
        
    #DBにデータを保存
    con.execute("INSERT INTO コメント(スレッドid, 内容, ユーザー名, 学籍番号 ,投稿時間)" +  f"values('{thread_id}', '{content}', '{user_name}', '{student_num}', datetime('now','localtime'))")

    con.commit()
    con.close()

#スレッドidに応じたスレッドの内容をjsonファイルへ保存
def comment_get_id(thread_id):
    con = sqlite3.connect(content_db)

    thread_content = con.execute(f"SELECT * FROM コメント WHERE スレッドid = {thread_id}").fetchall()

    #jsonデータのkeyを設定
    dict_item = ["id", "スレッドid", "内容", "ユーザー名", "学籍番号","投稿時間"]
    result = []

    #{key : item}の形式で辞書型リストに格納
    for item in thread_content:
        result.append(dict(zip(dict_item, item)))

    #jsonファイルに書き込み
    with open('./json/thread_id_content.json', 'w') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


    con.commit()
    con.close()


def Delete_Comment(Comment_ID, User_name):
    # DB接続。
    con = sqlite3.connect(content_db)

    #DBにあるコメント作成者のユーザー名を取得する
    check = con.execute(f"SELECT ユーザー名 FROM コメント WHERE id = {Comment_ID}").fetchone()[0]

    #コメントの作成者が削除できる
    if check == User_name:
        con.execute(f"DELETE from コメント WHERE id = {Comment_ID}")

        con.execute(f"UPDATE コメント SET id = (id - 1) WHERE id > {Comment_ID}")



    con.commit()

    con.close()




if __name__ == "__main__":
    comment_add(thread_id=4,content="www",user_name="nikoniko",student_num="k88888kk")
    #comment_get_id(1)