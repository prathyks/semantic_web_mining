import requests
import SQLFunctions
import SQLConnect
import logging
from bs4 import BeautifulSoup

logging.basicConfig(filename='crawler.log', level=logging.WARN)



def get_users_from_page(soup_obj):
    list_u = []
    table_tag = soup_obj.find('table', {'cellspacing': '1', 'class': 'trust'})
    trs = table_tag.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) > 1:
            name_id = tds[1].a["href"].split("_")[-1]
            name_tag = tds[1].a.text
            list_u.append((name_tag, name_id))
    return list_u


def get_users(member_id, mem_name):
    list_u = []
    url = 'http://www.ciao.co.uk/member_view.php/MemberId/' + str(member_id) + '/TabId/5'
    res = requests.get(url)
    plain_text = res.text
    soup_obj = BeautifulSoup(plain_text)
    tr_tag = soup_obj.find('tr', {'id': 'member_details_trusted_by'})
    num_of_trusted = int(tr_tag.contents[3].contents[0].split(' ', 1)[0])
    if num_of_trusted == 0:
        return list_u
    list_u = get_users_from_page(soup_obj)
    print("friends for "+mem_name+"("+str(member_id)+"):"+str(num_of_trusted))
    logging.warn("friends for "+mem_name+"("+str(member_id)+"):"+str(num_of_trusted))
    pages = int(num_of_trusted / 15)
    if num_of_trusted % 15 > 0:
        pages += 1
    if pages == 1:
        return list_u
    for i in range(2, pages+1):
        ind = (i-1) * 15
        page_url = url + "/Start/"+str(ind)
        #print(page_url)
        res = requests.get(page_url)
        soup_obj = BeautifulSoup(res.text)
        list_u += get_users_from_page(soup_obj)
    return list_u


def is_valid_user(user_id):
    url = 'http://www.ciao.co.uk/member_view.php/MemberId/' + str(user_id)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup_o = BeautifulSoup(plain_text)
    tr_tag = soup_o.find('tr', {'id': 'member_details_trusted_by'})
    if tr_tag is None:
        return False
    else:
        return True


def find_all_friends():
    conn = SQLConnect.mysql_connect()
    while True:
        res = SQLFunctions.get_all_non_scanned_users(conn)
        if len(res) == 0:
            logging.warn("------DONE------")
            print("------DONE------")
            break
        logging.warn("unscanned users:"+str(len(res)))
        for item in res:
            print("item:"+str(item[0]))
            user_list = get_users(item[0], item[1])
            for user in user_list:
                if SQLFunctions.does_user_exists(conn, user[1]) is True:
                    print(user[0]+" already exists")
                    continue
                if is_valid_user(user[1]) is False:
                    print("adding deleted user "+user[0]+","+str(user[1]))
                    logging.warn("adding deleted user "+user[0]+","+str(user[1])+" TRUE")
                    SQLFunctions.add_new_user(conn, user[1], user[0], True, False)
                else:
                    print("adding user "+user[0]+","+str(user[1]))
                    logging.warn("adding user "+user[0]+","+str(user[1])+" FALSE")
                    SQLFunctions.add_new_user(conn, user[1], user[0], False, False)
            SQLFunctions.update_scanned(conn, item[0])
            print("Processed: "+item[1]+", "+str(item[0]))
            logging.warn("Processed: "+item[1]+", "+str(item[0]))


find_all_friends()