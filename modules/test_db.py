

#ログイン機能デバッグ用

import sqlite3  #DB使用のためのimport文
import json

def new_user(user_name, password):
    
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/user.db')

    #テーブル(表)があるか確認
    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
    # print(table_count) #デバック

    if table_count == 0: #なかったらテーブルを作成して追加
        
        #テーブル作成SQL文
        con.execute("CREATE TABLE ユーザ一覧(ユーザID INTEGER PRIMARY KEY, ユーザ名 STRING" +
                        ", パスワード STRING)")

        #新規作成した時ユーザIDが0のため1を代入
        count = 1

        #テーブル追加SQL文
        con.execute("INSERT INTO ユーザ一覧(ユーザID, ユーザ名, パスワード)" +
                        f" values('{count}', '{user_name}', '{password}')")

    else: #あったらユーザの個数を取得して追加する

        #ユーザの数を確認
        user_count = con.execute("SELECT count(ユーザID) FROM ユーザ一覧")
        count = int(user_count.fetchone()[0])

        #一番高いユーザIDを作成
        count += 1

        #テーブル追加SQL文
        con.execute("INSERT INTO ユーザ一覧(ユーザID, ユーザ名, パスワード)" +
                        f" values('{count}', '{user_name}', '{password}')")

    con.commit()
    con.close()

    return count

def Get_user_All():
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/user.db')

    #テーブル(表)があるか確認
    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0]

    if table_count == 0:
        #テーブル作成SQL文
        con.execute("CREATE TABLE ユーザ一覧(ユーザID INTEGER PRIMARY KEY, ユーザ名 STRING" +
                        ", パスワード STRING)")
    
    #ユーザ全ての内容を取得
    get_all = con.execute("SELECT * FROM ユーザ一覧").fetchall()

    results = []

    #ユーザの内容を一つずつ取る
    for i in get_all:
        results.append(dictionary(list(i)))

    #ユーザIDを鍵とした辞書型を作成
    all_results = dict(results)

    #jsonファイル作成
    with(open('./json/All_user.json','w')) as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)

    con.commit()

    con.close()





def Get_user_One(user_id):
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/user.db')

    #テーブル(表)があるか確認
    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0]

    if table_count == 0:
        #テーブル作成SQL文
        con.execute("CREATE TABLE ユーザ一覧(ユーザID INTEGER PRIMARY KEY, ユーザ名 STRING" +
                        ", パスワード STRING)")

    #ユーザIDの内容を取得
    get_one = con.execute(f"SELECT * FROM ユーザ一覧 WHERE ユーザID = {user_id}").fetchone()
    
    results = []
    if get_one is not None:
        results.append(dictionary(list(get_one)))
    # print(get_one)

    #ユーザIDを鍵とした辞書型を作成
    one_results = dict(results)

    #jsonファイル作成
    with(open('./json/One_user.json','w')) as f:
        json.dump(one_results, f, indent=4, ensure_ascii=False)

    con.commit()

    con.close()


def dictionary(results: list):
    #辞書型の鍵の配列
    dict_item = ["ユーザID","ユーザー名", "パスワード"]
    array = []

    #先頭のユーザIDを取得して削除
    id = results.pop(0)

    #[ユーザID, 内容]の配列を作成
    array.extend([id, dict(zip(dict_item, results))])

    return array