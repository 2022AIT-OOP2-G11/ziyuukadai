import sqlite3  #DB使用のためのimport文

def new_thread(Thread_Name, Make_User_Name):
    
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/Thread.db')

    #スレッドの数を確認
    c = con.execute("SELECT * FROM sqlite_master WHERE type='table'")
    count = len(c.fetchall())

    if not count: #一つもなかったらテーブルを作成して追加
        #新規作成した時スレッドIDが0のため1を代入
        count = 1
        #テーブル作成SQL文
        con.execute("CREATE TABLE スレッド一覧(スレッドID INTEGER PRIMARY KEY, スレッド名 STRING" +
                        ", ユーザー名 STRING, 最終更新時間 TIMESTAMP, スレッドを立てた時間 TIMESTAMP)")
        #テーブル追加SQL文
        con.execute("INSERT INTO スレッド一覧(スレッドID, スレッド名, ユーザー名, 最終更新時間, スレッドを立てた時間)" +
                        f" values('{count}', '{Thread_Name}', '{Make_User_Name}' ,datetime('now', 'localtime')" +
                            ", datetime('now', 'localtime'))")
    else: #あったらスレッドの個数を取得して追加する
        count += 1#一番高いスレッドIDを作成
        #テーブル追加SQL文
        con.execute("INSERT INTO スレッド一覧(スレッドID, スレッド名, ユーザー名, 最終更新時間, スレッドを立てた時間)" +
                        f" values('{count}', '{Thread_Name}', '{Make_User_Name}' ,datetime('now', 'localtime')" +
                            ", datetime('now', 'localtime'))")


    con.commit()
    




if __name__ == "__main__":
    new_thread(Thread_Name="愛工大", Make_User_Name="tomo")
