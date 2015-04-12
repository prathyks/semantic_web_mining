__author__ = 'udayrakesh'
import pymysql
pymysql.install_as_MySQLdb()

def mysql_connect():
    conn = pymysql.connect(host='localhost', port=3306, db='ciao', passwd='Pa$$w0rd', user='root');
    return conn

def mysql_close(con):
    con.close();
    return

def mysql_execute(conn, query):
    cur = conn.cursor();
    cur.execute(query)
    cur.close();
    conn.commit();
    return conn

def mysql_select_query(conn, query):
    cur = conn.cursor();
    cur.execute(query)
    return cur

def create_prod(conn):
    cur=conn.cursor();
    cur.execute('create table if not exists product(prod_id bigint(20) unsigned, prod_name varchar(150),product_category varchar(150),product_subcategory varchar(150), primary key(prod_id))ENGINE=InnoDB DEFAULT CHARSET=latin1')
    cur.execute('commit')

def create_review(conn) :
    cur=conn.cursor();
    cur.execute('create table if not exists review(review_id bigint(20) unsigned,review_name varchar(150) collate utf8_unicode_ci,review_rating float(5,2),review_date date,review_content varchar(10000) collate utf8_unicode_ci, product_id bigint(20), user_id bigint(20), primary key(review_id,user_id))')
    cur.execute('commit')

def add_product(conn,id,name,category,s_category):
    cur=conn.cursor()
    cur.execute("insert into product values("+id+",'"+name+"','"+category+"','"+s_category+"')")
    cur.execute('commit')

def add_review(conn,id,name,rating,date,content,p_id,u_id):
    cur=conn.cursor()
    cur.execute("insert into review values("+id+",'"+name+"',"+rating+",'"+date+"','"+content+"',"+p_id+","+u_id+")")
    cur.execute('commit')

def getUserCount(conn):
    query = "select count(*) from userinfo;"
    cur=conn.cursor()
    cur.execute(query)
    count = cur.fetchone()[0]
    print(count)
    cur.close()
    return count
