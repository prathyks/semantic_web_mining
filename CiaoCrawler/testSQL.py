import pymysql
import SQLFunctions
import SQLConnect
pymysql.install_as_MySQLdb()

conn = SQLConnect.mysql_connect();
count = SQLFunctions.getUserCount(conn);
print(count)

