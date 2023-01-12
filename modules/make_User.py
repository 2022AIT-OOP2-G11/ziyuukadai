import sqlite3
import json

# テーブル名 : ユーザー
# id        ユーザ名	  学籍番号	  パスワード
# 1,2...     String      String     String

# connect_db -> スレッドに接続する。もし、テーブルがなければテーブルを作成(引数なし)
# user_add -> ユーザを追加(引数 : ユーザ名, 学籍番号, パスワード)
# get_all_users -> 全てのユーザーをjsonファイルへ保存(引数なし)
# get_id_by_user -> idからユーザを取得(json)(引数 : id)
# get_studentnumber_by_user -> 学籍番号からユーザを取得(json)

# delete_user -> 学籍番号とパスワードからユーザをDBから削除する(引数 : 学籍番号, パスワード)



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

def dictionary(results: list):
    #辞書型の鍵の配列
    dict_item = ["ユーザー名", "学籍番号", "パスワード"]
    array = []

    #先頭のスレッドIDを取得して削除
    id = results.pop(0)

    #[スレッドID, 内容]の配列を作成
    array.extend([id, dict(zip(dict_item, results))])

    return array

#全てのユーザを取得
def get_all_users():
    con = connect_db()

    all_users = con.execute(f"SELECT * FROM ユーザー").fetchall()

    results = []
    for i in all_users:
        results.append(dictionary(list(i)))

    #スレッドIDを鍵とした辞書型を作成
    one_results = dict(results)

    #jsonファイル作成
    with(open('./json/All_Users.json','w')) as f:
        json.dump(one_results, f, indent=4, ensure_ascii=False)

    con.commit()

    con.close()




#idからユーザを取得
def get_id_by_user(id):
    con = connect_db()

    id_by_users = con.execute(f"SELECT * FROM ユーザー WHERE id = {id}").fetchone()

    results = []
    if id_by_users is not None:
        results.append(dictionary(list(id_by_users)))

    #スレッドIDを鍵とした辞書型を作成
    one_results = dict(results)

    #jsonファイル作成
    with(open('./json/Id_by_Users.json','w')) as f:
        json.dump(one_results, f, indent=4, ensure_ascii=False)

    con.commit()

    con.close()





#学籍番号からユーザを取得
def get_studentnumber_by_user(student_number):
    con = connect_db()

    studentnumber_by_users = con.execute(f"SELECT * FROM ユーザー WHERE 学籍番号 = '{student_number}'").fetchone()
    # print(studentnumber_by_users)

    results = []

    if studentnumber_by_users is not None:
        results.append(dictionary(list(studentnumber_by_users)))

    #スレッドIDを鍵とした辞書型を作成
    one_results = dict(results)

    #jsonファイル作成
    with(open('./json/Num_by_Users.json','w')) as f:
        json.dump(one_results, f, indent=4, ensure_ascii=False)

    con.commit()

    con.close()

#学籍番号とパスワードでユーザを削除
def delete_user(student_number, password):
    con = connect_db()

    con.execute(f"DELETE FROM ユーザー WHERE 学籍番号 = '{student_number}' and パスワード = '{password}'")
    #con.execute(f"UPDATE ユーザ SET id = (id - 1) WHERE id > {Thread_ID}")

    get_all_users()

    con.commit()
    con.close()
    












