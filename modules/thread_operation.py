import sqlite3  #DB使用のためのimport文
import json

#スレッド新規作成
def new_thread(Thread_Name, Make_User_Name):
    
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/DataBase.db')

    #テーブル(表)があるか確認
    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='スレッド一覧'").fetchone()[0]
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

#全てのスレッドをjsonで取得
def Get_Thread_All():
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/DataBase.db')

    #テーブル(表)があるか確認
    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='スレッド一覧'").fetchone()[0]

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




#引数のスレッドIDのスレッドを取得
def Get_Thread_One(Thread_ID):
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/DataBase.db')

    #テーブル(表)があるか確認
    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='スレッド一覧'").fetchone()[0]

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

#辞書型にする関数
def dictionary(results: list):
    #辞書型の鍵の配列
    dict_item = ["スレッド名", "ユーザー名", "最終更新時間", "スレッドを立てた時間"]
    array = []

    #先頭のスレッドIDを取得して削除
    id = results.pop(0)

    #[スレッドID, 内容]の配列を作成
    array.extend([id, dict(zip(dict_item, results))])

    return array

#更新時間の更新
def Update_Thread_Time(Thread_ID):
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/DataBase.db')

    con.execute(f"UPDATE スレッド一覧 SET 最終更新時間 = datetime('now', 'localtime') WHERE スレッドID = {Thread_ID}")

    con.commit()

    con.close()

#引数にスレッドIDとスレッドを消そうとしてるユーザー名をいれ、スレッドの作成者と消そうとしてるユーザー名の時は消せるようにし、
#違ったら消せないようにする
def Delete_One_Thread(Thread_ID, User_name):
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/DataBase.db')

    #DBにあるスレッド作成者のユーザー名を取得する
    check = con.execute(f"SELECT ユーザー名 FROM スレッド一覧 WHERE スレッドID = {Thread_ID}").fetchone()[0]

    #スレッドの作成者が削除できる
    if check == User_name:
        con.execute(f"DELETE from スレッド一覧 WHERE スレッドID = {Thread_ID}")

        con.execute(f"UPDATE スレッド一覧 SET スレッドID = (スレッドID - 1) WHERE スレッドID > {Thread_ID}")

        message = "削除できました"

    else:

        message = "作成者ではないため削除できません"


    con.commit()

    con.close()

    return message

#スレッド検索関数
def Search_Thread_Name(word: str):
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/DataBase.db')

    #テーブル(表)があるか確認
    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='スレッド一覧'").fetchone()[0]

    if table_count == 0:
        #テーブル作成SQL文
        con.execute("CREATE TABLE スレッド一覧(スレッドID INTEGER PRIMARY KEY, スレッド名 STRING" +
                        ", ユーザー名 STRING, 最終更新時間 TIMESTAMP, スレッドを立てた時間 TIMESTAMP)")

    search_word_list = word.split()
    word_len = len(search_word_list)
    escape_flag = False
    time = 0

    search_sql = "SELECT * FROM スレッド一覧 WHERE"

    for search_word in search_word_list:

        time += 1

        if('%' in search_word):
            escape_flag = True
            wild_num = search_word.find('%')
            word_list = list(search_word)
            word_list.insert(wild_num, '¥')
            search_word = "".join(word_list)

        if('_' in search_word):
            escape_flag = True
            wild_num = search_word.find('_')
            word_list = list(search_word)
            word_list.insert(wild_num, '¥')
            search_word = "".join(word_list)

        search_sql += f' スレッド名 LIKE \'%{search_word}%\''

        if word_len > 1 and word_len != time:
            search_sql += ' or'

    if escape_flag:
        search_sql += ' ESCAPE \'¥\''


    #スレッドIDの内容を取得
    get_search = con.execute(search_sql).fetchall()

    results = []
    if get_search is not None:
        #スレッドの内容を一つずつ取る
        for i in get_search:
            results.append(dictionary(list(i)))

    #スレッドIDを鍵とした辞書型を作成
    search_results = dict(results)
    

    #jsonファイル作成
    with(open('./json/Search_thread.json','w')) as f:
        json.dump(search_results, f, indent=4, ensure_ascii=False)

    con.commit()

    con.close()

#ユーザー検索
def Search_User_Name(word: str):
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/DataBase.db')

    #テーブル(表)があるか確認
    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='スレッド一覧'").fetchone()[0]

    if table_count == 0:
        #テーブル作成SQL文
        con.execute("CREATE TABLE スレッド一覧(スレッドID INTEGER PRIMARY KEY, スレッド名 STRING" +
                        ", ユーザー名 STRING, 最終更新時間 TIMESTAMP, スレッドを立てた時間 TIMESTAMP)")

    search_word_list = word.split()
    word_len = len(search_word_list)
    escape_flag = False
    time = 0

    search_sql = "SELECT * FROM スレッド一覧 WHERE"

    for search_word in search_word_list:

        time += 1

        if('%' in search_word):
            escape_flag = True
            wild_num = search_word.find('%')
            word_list = list(search_word)
            word_list.insert(wild_num, '¥')
            search_word = "".join(word_list)

        if('_' in search_word):
            escape_flag = True
            wild_num = search_word.find('_')
            word_list = list(search_word)
            word_list.insert(wild_num, '¥')
            search_word = "".join(word_list)

        search_sql += f' ユーザー名 LIKE \'%{search_word}%\''

        if word_len > 1 and word_len != time:
            search_sql += ' or'

    if escape_flag:
        search_sql += ' ESCAPE \'¥\''


    #スレッドIDの内容を取得
    get_search = con.execute('SELECT * FROM スレッド一覧 WHERE スレッド名 LIKE \'%%f%%\'').fetchall()

    results = []
    #スレッドの内容を一つずつ取る
    for i in get_search:
        results.append(dictionary(list(i)))

    #スレッドIDを鍵とした辞書型を作成
    search_results = dict(results)
    

    #jsonファイル作成
    with(open('./json/Search_User.json','w')) as f:
        json.dump(search_results, f, indent=4, ensure_ascii=False)

    con.commit()

    con.close()
    

if __name__ == "__main__":
    # new_thread(Thread_Name="ffff", Make_User_Name="そろ")
    # Get_Thread_All()
    # Get_Thread_One(2)
    # Update_Thread_Time(2)
    # print(Delete_One_Thread(2, "yug"))
    # Search_Thread_Name('f') 
    # Search_User_Name('とも')

    pass