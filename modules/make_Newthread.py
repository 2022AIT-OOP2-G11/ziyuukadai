import sqlite3  #DB使用のためのimport文

def new_thread(Thread_Name, Make_User_Name):
    
    # DB接続。ファイルがなければ作成する
    con = sqlite3.connect('./DB/Thread.db')




if __name__ == "__main__":
    pass
