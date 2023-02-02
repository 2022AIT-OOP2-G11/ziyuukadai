import sqlite3  #DB使用のためのimport文
import json

#スレッド新規作成
def new_thread(Thread_Name, Make_User_Name, Student_Num):
    
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/DataBase.db')

    #テーブル(表)があるか確認
    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='スレッド一覧'").fetchone()[0]
    # print(table_count) #デバック

    if table_count == 0: #なかったらテーブルを作成して追加
        
        #テーブル作成SQL文
        con.execute("CREATE TABLE スレッド一覧(スレッドID INTEGER PRIMARY KEY, スレッド名 STRING" +
                        ", ユーザー名 STRING, 学籍番号 STRING, 最終更新時間 TIMESTAMP, スレッドを立てた時間 TIMESTAMP)")

        #新規作成した時スレッドIDが0のため1を代入
        count = 1

        #テーブル追加SQL文
        con.execute("INSERT INTO スレッド一覧(スレッドID, スレッド名, ユーザー名, 学籍番号, 最終更新時間, スレッドを立てた時間)" +
                        f" values('{count}', '{Thread_Name}', '{Make_User_Name}', '{Student_Num}' ,datetime('now', 'localtime')" +
                            ", datetime('now', 'localtime'))")

    else: #あったらスレッドの個数を取得して追加する

        #スレッドの数を確認
        thread_count = con.execute("SELECT count(スレッドID) FROM スレッド一覧")
        count = int(thread_count.fetchone()[0])

        #一番高いスレッドIDを作成
        count += 1

        #テーブル追加SQL文
        con.execute("INSERT INTO スレッド一覧(スレッドID, スレッド名, ユーザー名, 学籍番号, 最終更新時間, スレッドを立てた時間)" +
                        f" values('{count}', '{Thread_Name}', '{Make_User_Name}', '{Student_Num}' ,datetime('now', 'localtime')" +
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
                        ", ユーザー名 STRING, 学籍番号 STRING, 最終更新時間 TIMESTAMP, スレッドを立てた時間 TIMESTAMP)")
    
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
                        ", ユーザー名 STRING, 学籍番号 STRING, 最終更新時間 TIMESTAMP, スレッドを立てた時間 TIMESTAMP)")

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
    dict_item = ["スレッド名", "ユーザー名", "学籍番号", "最終更新時間", "スレッドを立てた時間"]
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
def Delete_One_Thread(Thread_ID, Student_Num):
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/DataBase.db')

    #DBにあるスレッド作成者のユーザー名を取得する
    check = con.execute(f"SELECT 学籍番号 FROM スレッド一覧 WHERE スレッドID = {Thread_ID}").fetchone()[0]

    #スレッドの作成者が削除できる
    if check == Student_Num:
        con.execute(f"DELETE from スレッド一覧 WHERE スレッドID = {Thread_ID}")

        con.execute(f"UPDATE スレッド一覧 SET スレッドID = (スレッドID - 1) WHERE スレッドID > {Thread_ID}")

        message = "削除できました"

    else:

        message = "作成者ではないため削除できません"


    con.commit()

    con.close()

    return message

#スレッド検索関数
def Search_Thread(word: str):
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/DataBase.db')

    #テーブル(表)があるか確認
    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='スレッド一覧'").fetchone()[0]

    if table_count == 0:
        #テーブル作成SQL文
        con.execute("CREATE TABLE スレッド一覧(スレッドID INTEGER PRIMARY KEY, スレッド名 STRING" +
                        ", ユーザー名 STRING, 学籍番号 STRING, 最終更新時間 TIMESTAMP, スレッドを立てた時間 TIMESTAMP)")

    
    #スレッド検索とユーザ名検索分割
    word_list = word.split(' | ')
    #スレッド検索の文字列を変数に入れる
    search_thread_word = word_list[0]
    #ユーザー名検索の文字列を変数に入れる
    search_user_word = word_list[1]
    #スレッド又はユーザー名で検索するかしないかのフラグ(最初はFalse)
    search_thread_flag = False
    search_user_flag = False
    
    #スレッド検索文字分割(空白を入れて検索した時に別れた文字をorで検索する)
    search_thread_word_list = search_thread_word.split()
    #検索文字列があるか確認
    word_len = len(search_thread_word_list)
    #SQLにワイルドカードがあった時に「ESCAPE」を追加するようにするフラグ
    escape_flag = False
    #スレッド検索文字のどこの文字のSQL文を作っているかの確認変数
    time = 0

    #スレッド検索文字が1つ以上あったらSQL文を作成
    if word_len > 0:
        #スレッドの検索をするのでフラグにTrueを代入
        search_thread_flag = True
        #SQL文の最初
        search_thread_sql = "SELECT * FROM スレッド一覧 WHERE"

        #分割した文字をリストから一つずつ取り出してSQL文作成
        for search_word in search_thread_word_list:
            #スレッド検索文字のどこの文字のSQL文を作っているかの確認変数に1を足す
            time += 1

            #検索文字の中に「%」が入っていたとき
            if('%' in search_word):
                #「%」はワイルドカードのため「ESCAPE」フラグにTrueを代入
                escape_flag = True
                #「%」の場所が文字列の左から何番目かを取得
                wild_num = search_word.find('%')
                #文字列を一文字ずつのlistにする
                word_list = list(search_word)
                #insertの引数に「%」の場所の番号とエスケープ文字を代入することで
                #%の前にエスケープ文字を代入する
                word_list.insert(wild_num, '¥')
                #listを文字列に直して検索文字列変数に代入
                search_word = "".join(word_list)

            if('_' in search_word):
                #「_」はワイルドカードのため「ESCAPE」フラグにTrueを代入
                escape_flag = True
                #「_」の場所が文字列の左から何番目かを取得
                wild_num = search_word.find('_')
                #文字列を一文字ずつのlistにする
                word_list = list(search_word)
                #insertの引数に「_」の場所の番号とエスケープ文字を代入することで
                #%の前にエスケープ文字を代入する
                word_list.insert(wild_num, '¥')
                #listを文字列に直して検索文字列変数に代入
                search_word = "".join(word_list)

            #検索文字がスレッド名のどこかに含まれていたら結果としてすSQL文
            search_thread_sql += f' スレッド名 LIKE \'%{search_word}%\''

            #検索文字が1つより多くて作成したSQL文が最後の検索文字でない時
            if word_len > 1 and word_len != time:
                #SQL文に「or」を追加
                search_thread_sql += ' or'
        #最後にエスケーブ文字を使用した時に必要なSQL文を追加
        if escape_flag:
            search_thread_sql += ' ESCAPE \'¥\''

    #ユーザ名検索文字分割(空白を入れて検索した時に別れた文字をorで検索する)
    search_user_word_list = search_user_word.split()
    #検索文字列があるか確認
    word_len = len(search_user_word_list)
    #SQLにワイルドカードがあった時に「ESCAPE」を追加するようにするフラグ
    escape_flag = False
    #ユーザー名検索文字のどこの文字のSQL文を作っているかの確認変数
    time = 0

    #ユーザー名検索文字が1つ以上あったらSQL文を作成
    if word_len > 0:
        #ユーザー名の検索をするのでフラグにTrueを代入
        search_user_flag = True
        #SQL文の最初
        search_user_sql = "SELECT * FROM スレッド一覧 WHERE"

        #分割した文字をリストから一つずつ取り出してSQL文作成
        for search_word in search_user_word_list:
            #ユーザー名検索文字のどこの文字のSQL文を作っているかの確認変数に1を足す
            time += 1

            #検索文字の中に「%」が入っていたとき
            if('%' in search_word):
                #「%」はワイルドカードのため「ESCAPE」フラグにTrueを代入
                escape_flag = True
                #「%」の場所が文字列の左から何番目かを取得
                wild_num = search_word.find('%')
                #文字列を一文字ずつのlistにする
                word_list = list(search_word)
                #insertの引数に「_」の場所の番号とエスケープ文字を代入することで
                #%の前にエスケープ文字を代入する
                word_list.insert(wild_num, '¥')
                #listを文字列に直して検索文字列変数に代入
                search_word = "".join(word_list)

            if('_' in search_word):
                #「_」はワイルドカードのため「ESCAPE」フラグにTrueを代入
                escape_flag = True
                #「_」の場所が文字列の左から何番目かを取得
                wild_num = search_word.find('_')
                #文字列を一文字ずつのlistにする
                word_list = list(search_word)
                #insertの引数に「_」の場所の番号とエスケープ文字を代入することで
                #%の前にエスケープ文字を代入する
                word_list.insert(wild_num, '¥')
                #listを文字列に直して検索文字列変数に代入
                search_word = "".join(word_list)

            #検索文字がユーザー名のどこかに含まれていたら結果としてすSQL文
            search_user_sql += f' ユーザー名 LIKE \'%{search_word}%\''

            #検索文字が1つより多くて作成したSQL文が最後の検索文字でない時
            if word_len > 1 and word_len != time:
                #SQL文に「or」を追加
                search_user_sql += ' or'

        #最後にエスケーブ文字を使用した時に必要なSQL文を追加
        if escape_flag:
            search_user_sql += ' ESCAPE \'¥\''

    #スレッド名とユーザー名どちらも検索した時は「INTERSECT」でそれぞれ実行したSQL文の結果の共通するスレッド
    #が出るようにする
    if search_thread_flag and search_user_flag:
        search_sql = f"{search_thread_sql} INTERSECT {search_user_sql}"
    #スレッドのみを検索した時はそのまま検索SQL文として使用
    elif search_thread_flag:
        search_sql = search_thread_sql
    #ユーザー名のみを検索した時はそのまま検索SQL文として使用
    elif search_user_flag:
        search_sql = search_user_sql
    #どちらも検索しなかった場合全てのスレッドを表示
    else:
        search_sql = "SELECT * FROM スレッド一覧"


    #検索の結果を取得
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
    

if __name__ == "__main__":
    new_thread(Thread_Name="これはテスト", Make_User_Name="nikoniko", Student_Num="K88888KK")
    new_thread(Thread_Name="今日の朝ごはんは何！？", Make_User_Name="nikoniko", Student_Num="K88888KK")

    # Get_Thread_All()
    # Get_Thread_One(2)
    # Update_Thread_Time(2)
    #print(Delete_One_Thread(1, None))
    #Search_Thread_Name('f') 
    #Search_User_Name('tomo')
    pass
