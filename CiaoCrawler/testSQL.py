import pymysql
import SQLFunctions
import SQLConnect
import requests
import logging
from bs4 import BeautifulSoup
pymysql.install_as_MySQLdb()
import sys

from datetime import date
from dateutil.rrule import rrule, DAILY


logging.basicConfig(filename='crawler.log', level=logging.WARN)


def login():
    auth_info = {"login_name": "prathyks", "login_password": "pass123"}
    url_s = "https://www.ciao.co.uk/login.php"
    sess.post(url_s, auth_info)


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


def get_users_in_page(html_text):
    user_list = []
    soup_obj = BeautifulSoup(html_text)
    alltds = soup_obj.find_all('td', {'class': 'noWrap'})
    for td in alltds:
        if td.a is None:
            continue
        else:
            a_href = td.a['href']
            split_parts = a_href.split("_")
            name_id = split_parts[-1]
            name_tag = split_parts[-2]
            user_list.append((name_tag, name_id))
    return user_list


def remove_dup(seq, idfun=None):
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result


#print(is_valid_user(12))
#print(is_valid_user(24))

#a = date(2015, 3, 27)
date_t = sys.argv[1]
year = int(date_t[0:4])
month = int(date_t[4:6])
day = int(date_t[6:8])
b = date(year, month, day)
#b = date(2010, 4, 19)
a = date(2015, 3, 27)
sess = requests.session()
login()
for dt in rrule(DAILY, dtstart=b, until=a):
    list_u = []
    date_str = dt.strftime("%Y%m%d")
    f_hand = open('last_date', 'w')
    f_hand.write(date_str)
    f_hand.close()
    url = "http://www.ciao.co.uk/opinions_archive_"+date_str+".html"
    print("date:"+date_str)
    logging.warn("date:"+date_str)
    res = sess.get(url)
    soup_obj = BeautifulSoup(res.text)
    td_cont = soup_obj.find('td', {'class': 'rangearticles'})
    if td_cont is None:
        continue
    if len(td_cont.text.strip()) == 0:
        continue
    temp_list = get_users_in_page(res.text)
    for x in temp_list:
        list_u.append(x)
    #print(td_cont)
    num_reviews = int(td_cont.text.split(" ")[-2])
    pages = int(num_reviews / 25)
    if num_reviews % 25 != 0:
        pages += 1
    if pages > 1:
        for i in range(2, pages+1):
            ind = (i-1) * 25
            url = "http://www.ciao.co.uk/site_index.php/Type/3/Date/"+date_str+"/Start/"+str(ind)
            #print(url)
            res = sess.get(url)
            temp_list = get_users_in_page(res.text)
            for x in temp_list:
                list_u.append(x)
    list_u = remove_dup(list_u)
    conn = SQLConnect.mysql_connect()
    for x in list_u:
        if SQLFunctions.does_user_exists(conn, x[1]) is True:
            print(x[0]+" already exists")
            continue
        if is_valid_user(x[1]) is False:
            print("adding deleted user "+x[0]+","+str(x[1]))
            logging.warn("adding deleted user "+x[0]+","+str(x[1])+" TRUE")
            SQLFunctions.add_user(conn, x[1], x[0], True)
        else:
            print("adding user "+x[0]+","+str(x[1]))
            logging.warn("adding user "+x[0]+","+str(x[1])+" FALSE")
            SQLFunctions.add_user(conn, x[1], x[0], False)