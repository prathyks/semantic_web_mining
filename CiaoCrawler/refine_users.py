import requests
import SQLFunctions
import SQLConnect
from bs4 import BeautifulSoup

conn = SQLConnect.mysql_connect()
res = SQLFunctions.get_all_users(conn)
for item in res:
    url = 'http://www.ciao.co.uk/member_view.php/MemberId/' + str(item[0]) + '/TabId/5'
    try:
        source_code = requests.get(url)
    except ConnectionError as e:
        print(str(e)+" "+str(item[1]))
        continue
    except ConnectionResetError as e:
        print(str(e)+" "+str(item[1]))
        continue
    plain_text = source_code.text
    soup_obj = BeautifulSoup(plain_text)
    tr_tag = soup_obj.find('tr', {'id': 'member_details_trusted_by'})
    if tr_tag is None:
        print(str(item[0])+" deleted")
        SQLFunctions.delete_user(conn, item[0])
SQLConnect.mysql_close(conn)