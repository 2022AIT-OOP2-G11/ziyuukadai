import sqlite3  #DB使用のためのimport文
import json

def new_thread(Thread_Name, Make_User_Name):
    
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/Thread.db')

    #テーブル(表)があるか確認
    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
    # print(table_count) #デバック

    if table_count == 0: #なかったらテーブルを作成して追加
        
        #テーブル作成SQL文
        con.execute("CREATE TABLE スレッド一覧(スレッドID INTEGER PRIMARY KEY, スレッド名 STRING" +
                        ", ユーザー名 STRING, 最終更新時間 TIMESTAMP, スレッドを立てた時間 TIMESTAMP)")

        #新規作成した時スレッドIDが0のため1を代入
        count = 1

        #テーブル追加SQL文
        con.execute("INSERT INTO スレッド一覧(スレッドID, スレッド名, ユーザー名, 最終更新時間, スレッドを立てた時間)" +
                        f" values('{count}', '{Thread_Name}', '{Make_User_Name}' ,datetime('now', 'localtime')" +
                            ", datetime('now', 'localtime'))")

    else: #あったらスレッドの個数を取得して追加する

        #スレッドの数を確認
        thread_count = con.execute("SELECT count(スレッドID) FROM スレッド一覧")
        count = int(thread_count.fetchone()[0])

        #一番高いスレッドIDを作成
        count += 1

        #テーブル追加SQL文
        con.execute("INSERT INTO スレッド一覧(スレッドID, スレッド名, ユーザー名, 最終更新時間, スレッドを立てた時間)" +
                        f" values('{count}', '{Thread_Name}', '{Make_User_Name}' ,datetime('now', 'localtime')" +
                            ", datetime('now', 'localtime'))")


    con.commit()

    con.close()


def Get_Thread_All():
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/Thread.db')

    #テーブル(表)があるか確認
    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0]

    if table_count == 0:
        #テーブル作成SQL文
        con.execute("CREATE TABLE スレッド一覧(スレッドID INTEGER PRIMARY KEY, スレッド名 STRING" +
                        ", ユーザー名 STRING, 最終更新時間 TIMESTAMP, スレッドを立てた時間 TIMESTAMP)")
    
    #スレッド全ての内容を取得
    get_all = con.execute("SELECT * FROM スレッド一覧").fetchall()

    results = []

    #スレッドの内容を一つずつ取る
    for i in get_all:
        results.append(dictionary(list(i)))

    #スレッドIDを鍵とした辞書型を作成
    all_results = dict(results)

    #jsonファイル作成
    with(open('./json/All_thread.json','w')) as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)

    con.commit()

    con.close()





def Get_Thread_One(Thread_ID):
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/Thread.db')

    #テーブル(表)があるか確認
    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0]

    if table_count == 0:
        #テーブル作成SQL文
        con.execute("CREATE TABLE スレッド一覧(スレッドID INTEGER PRIMARY KEY, スレッド名 STRING" +
                        ", ユーザー名 STRING, 最終更新時間 TIMESTAMP, スレッドを立てた時間 TIMESTAMP)")

    #スレッドIDの内容を取得
    get_one = con.execute(f"SELECT * FROM スレッド一覧 WHERE スレッドID = {Thread_ID}").fetchone()
    
    results = []
    if get_one is not None:
        results.append(dictionary(list(get_one)))
    # print(get_one)

    #スレッドIDを鍵とした辞書型を作成
    one_results = dict(results)

    #jsonファイル作成
    with(open('./json/One_thread.json','w')) as f:
        json.dump(one_results, f, indent=4, ensure_ascii=False)

    con.commit()

    con.close()


def dictionary(results: list):
    #辞書型の鍵の配列
    dict_item = ["スレッド名", "ユーザー名", "最終更新時間", "スレッドを立てた時間"]
    array = []

    #先頭のスレッドIDを取得して削除
    id = results.pop(0)

    #[スレッドID, 内容]の配列を作成
    array.extend([id, dict(zip(dict_item, results))])

    return array


    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/Thread.db')

    #スレッドの数を確認
    c = con.execute("SELECT count(スレッドID) FROM スレッド一覧")

    # print(c.fetchone()[0])

    count = c.fetchone()[0]



    print(count)







    




if __name__ == "__main__":
    new_thread(Thread_Name="c", Make_User_Name="tomo")
    # Get_Thread_All()