import sqlite3
import json

# id	スレッドid	内容	ユーザー名	 投稿時間
# 1, 2,  int	 string	   string	YY:MM:DD:mm:ss　　

# connect_db -> スレッドに接続する。もし、テーブルがなければテーブルを作成(引数なし)
# comment_add -> コメントを追加(引数 : スレッドid, 内容, ユーザー名)
# comment_get_id -> スレッドidに応じたスレッドの内容をjsonファイルへ保存(引数 : thread_id)

content_db = './DB/content.db'

#指定されたスレッドのDBに接続し、テーブルが作成されていない場合作成
def connect_db():
    con = sqlite3.connect(content_db)

    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
    print(table_count)

    if table_count == 0:
        con.execute("CREATE TABLE コメント(id INTEGER PRIMARY KEY AUTOINCREMENT, スレッドid INTEGER NOT NULL, 内容 TEXT NOT NULL, ユーザー名 TEXT, 投稿時間 TIMESTAMP)")

#コメントを追加 → (スレッドid, 内容, ユーザー名)
def comment_add(thread_id, content, user_name): 
    con = sqlite3.connect(content_db)
    
    con.execute("INSERT INTO コメント(スレッドid, 内容, ユーザー名, 投稿時間)" +  f"values('{thread_id}', '{content}', '{user_name}', datetime('now','localtime'))")
    print("登録完了")
    con.commit()
    con.close()

#スレッドidに応じたスレッドの内容をjsonファイルへ保存
def comment_get_id(thread_id):
    con = sqlite3.connect(content_db)

    thread_content = con.execute(f"SELECT * FROM コメント WHERE スレッドid = {thread_id}").fetchall()

    dict_item = ["id", "スレッドid", "内容", "ユーザー名", "投稿時間"]
    result = []

    for item in thread_content:
        result.append(dict(zip(dict_item, item)))

    with open('./json/thread_id_content.json', 'w') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


    con.commit()
    con.close()



if __name__ == "__main__":
    connect_db()
    comment_add(1, "今日はいい天気", "Yuri")
    comment_get_id(1)






