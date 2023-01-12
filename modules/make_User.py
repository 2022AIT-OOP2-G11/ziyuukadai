import sqlite3
import json

# テーブル名 : ユーザー
# id        ユーザ名	  学籍番号	  パスワード
# 1,2...     String      String     String

# connect_db -> スレッドに接続する。もし、テーブルがなければテーブルを作成(引数なし)
# user_add -> ユーザを追加(引数 : ユーザ名, 学籍番号, パスワード)
# comment_get_id -> スレッドidに応じたスレッドの内容をjsonファイルへ保存(引数 : thread_id)

content_db = './DB/DataBase.db' #DBの保存場所

#指定されたスレッドのDBに接続し、テーブルが作成されていない場合作成
def connect_db():
    con = sqlite3.connect(content_db) #DBに接続

    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='ユーザー'").fetchone()[0]

    #テーブルが作成されていない場合は作成
    if table_count == 0:
        con.execute("CREATE TABLE ユーザー(id INTEGER PRIMARY KEY AUTOINCREMENT, ユーザ名 TEXT NOT NULL , \
            学籍番号 TEXT NOT NULL UNIQUE, パスワード TEXT NOT NULL UNIQUE)")

    return con

#ユーザを追加 → (ユーザ名, 学籍番号, パスワード)
def user_add(username, student_number, password): 
    con = connect_db()
    
    #DBにデータを保存
    con.execute("INSERT INTO ユーザー(ユーザ名, 学籍番号, パスワード)" +  f"values('{username}', '{student_number}', '{password}')")

    con.commit()
    con.close()

#全てのユーザを取得
def get_all_users():
    con = connect_db()


#idからユーザを取得


#学籍番号からユーザを取得











