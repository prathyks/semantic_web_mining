__author__ = 'VamshiKrishna', 'PrateekShankar'

import requests
import re
import time
import logging
from bs4 import BeautifulSoup
import SQLConnect
import SQLFunctions
import MostPopularUsers
from requests.exceptions import ConnectionError

logging.basicConfig(filename='crawler.log', level=logging.WARN)


def crawl_ciao():
    list_users = []
    temp_list = get_latest_reviewer_list()
    for x in temp_list:
        list_users.append(x)
    temp_list = MostPopularUsers.pop_and_recent_users()
    for x in temp_list:
        list_users.append(x)
    print("final_list:"+str(len(list_users)))
    for new_id in list_users:
        conn = SQLConnect.mysql_connect()
        if SQLFunctions.does_user_exists(conn, new_id[1]) is True:
            SQLConnect.mysql_close(conn)
            print(str(new_id[1])+" alredy exists")
            continue
        SQLConnect.mysql_close(conn)
        if is_valid_user(new_id[1]) is None:
            continue
        print("Found at:"+str(new_id[1]))
        member_id = [new_id]
        print("Starting from "+str(member_id[0][1]))
        user_iterate = 0
        for item in member_id:
            url = 'http://www.ciao.co.uk/member_view.php/MemberId/' + str(item[1]) + '/TabId/5'
            members_to_insert = [item]
            try:
                source_code = requests.get(url)
                #time.sleep(2)
            except ConnectionError as e:
                print(str(e)+" "+str(item[1]))
                continue
            except ConnectionResetError as e:
                print(str(e)+" "+str(item[1]))
                continue
            plain_text = source_code.text
            soup_obj = BeautifulSoup(plain_text)
            for_trusted_link = 0
            tr_tag = soup_obj.find('tr', {'id': 'member_details_trusted_by'})

            # Get the number of users trusted by
            try:
                num_of_trusted = int(tr_tag.contents[3].contents[0].split(' ', 1)[0])
            except AttributeError as e:
                print(str(e)+" "+str(item[1]))
                user_iterate += 1
                continue

            while num_of_trusted > 0:
                for a_tags in soup_obj.find_all('a', href=True):
                    a_href = a_tags['href']
                    match = re.search(r'http://www.ciao.co.uk/Member__*', a_href)
                    if match:
                        name_id = a_href.split('__', 1)[1].rsplit('_', 1)
                        name_id[0] = name_id[0].lower()
                        name_id = tuple(name_id)
                        if is_valid_user(name_id[1]) is None:
                            continue
                        member_id.append(name_id)
                        members_to_insert.append(name_id)
                if num_of_trusted > 15:
                    for_trusted_link += 15
                    url = 'http://www.ciao.co.uk/member_view.php/MemberId/' + member_id[user_iterate][1] + '/TabId/5/Start/' + str(for_trusted_link)
                    try:
                        source_code = requests.get(url)
                        #time.sleep(2)
                    except ConnectionError as e:
                        print(e)
                        continue
                    except ConnectionResetError as e:
                        print(e)
                        continue
                    plain_text = source_code.text
                    soup_obj = BeautifulSoup(plain_text)
                num_of_trusted = num_of_trusted - 15
            user_iterate = user_iterate + 1
            member_id = remove_dup(member_id)
            members_to_insert = remove_dup(members_to_insert)
            print("Member "+str(item[1])+" has "+str(len(members_to_insert))+" buddies")
            if len(members_to_insert) > 0:
                conn = SQLConnect.mysql_connect()
                for temp_item in members_to_insert:
                    print("Adding user:{"+str(temp_item[1])+", "+temp_item[0]+"}")
                    SQLFunctions.add_user(conn, temp_item[1], temp_item[0])
                #sql_count = SQLFunctions.getUserCount(conn)
                SQLConnect.mysql_close(conn)
                #print("current users in DB: "+str(sql_count))
                members_to_insert = []
            print(len(member_id))
        print(member_id)


#Remove Duplicates from list..
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


def is_valid_user(user_id):
    url = 'http://www.ciao.co.uk/member_view.php/MemberId/' + str(user_id)
    source_code = requests.get(url)
    #time.sleep(1)
    plain_text = source_code.text
    soup_obj = BeautifulSoup(plain_text)
    tr_tag = soup_obj.find('tr', {'id': 'member_details_trusted_by'})
    if tr_tag:
        #print("tr found, "+str(tr_tag)+" id:"+str(user_id))
        span_content = soup_obj.find('div', {'id': 'Node_BreadCrumb'}).findAll('span')[2]
        user_name = str(span_content).split()[3].strip()[:-7]
        #print('span_content:'+str(span_content))
        return user_name, user_id
    else:
        print("not found, id:"+str(user_id))
        return None


def get_latest_reviewer_list():
    list_users = []
    for x in range(1, 8):
        index = (x-1) * 15
        url = "http://www.ciao.co.uk/Recent_Reviews/Start/"+str(index)
        print(url)
        source_code = requests.get(url).text
        soup_obj = BeautifulSoup(source_code)
        rev_links = soup_obj.find_all('a', {'class': 'review', 'by': ""})
        links = []
        for review_url in rev_links:
            links.append(review_url['href'])
        for review_url in links:
            source_code = requests.get(review_url).text
            soup_obj = BeautifulSoup(source_code)
            content = soup_obj.find('div', {'id': 'OH_BingUserInfo'}).find('a', {'class': 'black'})
            user_id = content['href'].split("_")[-1]
            user_name = content['title']
            list_users.append((user_name, user_id))
    return list_users

crawl_ciao()