import sqlite3

def Create_tabe():
    conn = sqlite3.connect("Exchanged_Data.db")
    cur = conn.cursor()

    cur.execute("create table UserInfo (date text, name text, type text, money1 text, money2 text)")

    cur.close()
    conn.close()

def Insert_Info(date, name, type, money1, money2):
    conn = sqlite3.connect("Exchanged_Data.db")
    cur = conn.cursor()

    cur.execute('INSERT INTO UserInfo VALUES(:date, :name, :type, :money1, :money2);', {"date": date, "name": name, "type": type, "money1": money1, "money2": money2})
    conn.commit()

    cur.close()
    conn.close()

def Date_SeletData():
    list = []

    conn = sqlite3.connect("Exchanged_Data.db")
    cur = conn.cursor()

    cur.execute('SELECT date FROM UserInfo')

    list.clear()

    for row in cur:
        s = str(row).replace('(','').replace(')','').replace(',','').replace("'","")
        list.append(s)

    cur.close()
    conn.close()

    return list

def Name_SeletData():
    list = []

    conn = sqlite3.connect("Exchanged_Data.db")
    cur = conn.cursor()

    cur.execute('SELECT name FROM UserInfo')
    list.clear()
    for row in cur:
        s = str(row).replace('(','').replace(')','').replace(',','').replace("'","")
        list.append(s)

    cur.close()
    conn.close()

    return list

def Type_SeletData():
    list = []

    conn = sqlite3.connect("Exchanged_Data.db")
    cur = conn.cursor()

    cur.execute('SELECT type FROM UserInfo')
    list.clear()
    for row in cur:
        s = str(row).replace('(','').replace(')','').replace(',','').replace("'","")
        list.append(s)

    cur.close()
    conn.close()

    return list

def Money1_SeletData():
    list = []

    conn = sqlite3.connect("Exchanged_Data.db")
    cur = conn.cursor()

    cur.execute('SELECT money1 FROM UserInfo')
    list.clear()
    for row in cur:
        s = str(row).replace('(','').replace(')','').replace(',','').replace("'","")
        list.append(s)

    cur.close()
    conn.close()

    return list

def Money2_SeletData():
    list = []

    conn = sqlite3.connect("Exchanged_Data.db")
    cur = conn.cursor()

    cur.execute('SELECT money2 FROM UserInfo')
    list.clear()
    for row in cur:
        s = str(row).replace('(','').replace(')','').replace(',','').replace("'","")
        list.append(s)

    cur.close()
    conn.close()

    return list

def Remove_Data(date, name, type, money1, money2):
    conn = sqlite3.connect("Exchanged_Data.db")
    cur = conn.cursor()

    cur.execute('DELETE FROM UserInfo WHERE date = ? and name = ? and type = ? and money1 = ? and money2 = ?', (date, name, type, money1, money2,))
    conn.commit()

    cur.close()
    conn.close()





