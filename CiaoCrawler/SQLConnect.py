import pymysql
pymysql.install_as_MySQLdb()

def mysql_connect():
    conn = pymysql.connect(host='localhost', port=3306, user='ciao', passwd='pass123', db='ciao');
    return conn

def mysql_close(con):
    con.close();
    return

def mysql_execute(conn, query):
    cur = conn.cursor();
    cur.execute(query)
    cur.close()
    conn.commit()
    return conn

def mysql_select_query(conn, query):
    cur = conn.cursor();
    cur.execute(query)
    return cur





