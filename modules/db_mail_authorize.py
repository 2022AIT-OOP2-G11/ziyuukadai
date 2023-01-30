
import sqlite3 
import json

#メール認証で使うためのテーブル

#スレッド新規作成
def new_temp_user(tmp_user:dict):
    
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/DataBase.db')

    #テーブル(表)があるか確認
    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='スレッド一覧'").fetchone()[0]
    # print(table_count) #デバック

    if table_count == 0: #なかったらテーブルを作成して追加
        
        #テーブル作成SQL文
        con.execute("CREATE TABLE 認証メール(ID INTEGER PRIMARY KEY, ユーザ名 STRING" +
                        ", 学籍番号 STRING UNIQUE, パスワード STRING, 認証コード STRING, 送信時間 TIMESTAMP, 送信回数 INTEGER)")

        #新規作成した時スレッドIDが0のため1を代入
        count = 1

        #テーブル追加SQL文
        con.execute("INSERT INTO 認証メール(ID, ユーザ名, 学籍番号, パスワード, 認証コード, 送信時間, 送信回数)" +
                    f" values('{count}', '{tmp_user['user_name']}', '{tmp_user['student_id']}', '{tmp_user['password']}',  '{tmp_user['authorize_num']}', datetime('now', 'localtime'), {tmp_user['count']})"
                    )

    else: #あったらスレッドの個数を取得して追加する

        #スレッドの数を確認
        thread_count = con.execute("SELECT count(ID) FROM 認証メール")
        count = int(thread_count.fetchone()[0])

        #一番高いスレッドIDを作成
        count += 1

        #テーブル追加SQL文
        con.execute("INSERT INTO 認証メール(ID, ユーザ名, 学籍番号, パスワード, 認証コード, 送信時間, 送信回数)" +
                        f" values('{count}', '{tmp_user['user_name']}', '{tmp_user['student_id']}', '{tmp_user['password']}',  '{tmp_user['authorize_num']}', datetime('now', 'localtime'), {tmp_user['count']})"
                    )

    con.commit()

    con.close()
    

#引数のスレッドIDのスレッドを取得
def get_mail_data(student_num):
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/DataBase.db')

    #テーブル(表)があるか確認
    table_count = con.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='認証メール'").fetchone()[0]

    if table_count == 0:
        #テーブル作成SQL文
         con.execute("CREATE TABLE 認証メール(ID INTEGER PRIMARY KEY, ユーザ名 STRING" +
                        ", 学籍番号 STRING UNIQUE, パスワード STRING, 認証コード STRING, 送信時間 TIMESTAMP, 送信回数 INTEGER)")

    #スレッドIDの内容を取得
    # try:
    data_array = con.execute(f"SELECT * FROM 認証メール WHERE 学籍番号 = '{student_num}'").fetchone()
    # except sqlite3.OperationalError :
    #     #みつからなかった時の処理
    #     data_array = None
   
    mail_data = None
    if data_array: 
        mail_data = {}
        mail_data["id"] = data_array[0]
        mail_data["user_name"] = data_array[1]
        mail_data["student_num"] = data_array[2]    
        mail_data["password"] = data_array[3]
        mail_data["authorize_num"] = data_array[4]
        mail_data["send_time"] = data_array[5]
        mail_data["count"] = data_array[6]

    con.commit()
    con.close()
    
    return mail_data

def delete_mail_data(id):
        con = sqlite3.connect('./DB/DataBase.db')
        con.execute(f"DELETE from 認証メール WHERE ID = {id}")
        con.execute(f"UPDATE 認証メール SET ID = (ID - 1) WHERE ID > {id}")
        con.commit()
        con.close()