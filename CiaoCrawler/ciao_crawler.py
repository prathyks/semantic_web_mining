__author__ = 'VamshiKrishna'

import requests
import re
import time
from bs4 import BeautifulSoup
import SQLConnect
import SQLFunctions
from requests.exceptions import ConnectionError

def crawl_ciao():
    member_id = [('richada','5515635')]
    membersToInsert = [];
    total = 50000;
    countInserted = 0;
    user_iterate = 0
    while countInserted < total:
        url = 'http://www.ciao.co.uk/member_view.php/MemberId/' + member_id[user_iterate][1] + '/TabId/5'
        try:
            source_code = requests.get(url)
            time.sleep(2)
        except ConnectionError as e:
            print(e)
            continue
        except ConnectionResetError as e:
            print(e)
            continue
        plain_text = source_code.text
        #print(plain_text)
        soup_obj = BeautifulSoup(plain_text)
        count = 0
        for_trusted_link = 0
        tr_tag = soup_obj.find('tr', {'id':'member_details_trusted_by'})

        # Get the number of users trusted by
        try:
            num_of_trusted = int(tr_tag.contents[3].contents[0].split(' ',1)[0])
        except AttributeError as e:
            print(e)
            user_iterate = user_iterate + 1
            continue

        while num_of_trusted > 0:
            for a_tags in soup_obj.find_all('a', href=True):
                a_href = a_tags['href']
                match = re.search(r'http://www.ciao.co.uk/Member__*', a_href)
                if match:
                    #count=count+1
                    name_id = a_href.split('__',1)[1].rsplit('_',1)
                    name_id[0] = name_id[0].lower()
                    name_id = tuple(name_id)
                    member_id.append(name_id)
                    membersToInsert.append(name_id);
            if(num_of_trusted > 15):
                for_trusted_link = for_trusted_link + 15
                url = 'http://www.ciao.co.uk/member_view.php/MemberId/' + member_id[user_iterate][1] + '/TabId/5/Start/' + str(for_trusted_link)
                try:
                    source_code = requests.get(url)
                    time.sleep(2)
                except ConnectionError as e:
                    print(e)
                    continue
                except ConnectionResetError as e:
                    print(e)
                    continue
                plain_text = source_code.text
                #count = count+1
                #print(count)
                soup_obj = BeautifulSoup(plain_text)
            num_of_trusted = num_of_trusted - 15

        user_iterate = user_iterate + 1
        #print(len(member_id))
        member_id = remove_dup(member_id)
        if len(membersToInsert) > 500:
            # string = 'output_' + str(user_iterate) + '.txt'
            # f = open(string,'w')
            # for item in member_id:
            #     f.write("%s," %item[0])
            #     f.write("%s\n" %item[1])
            # f.close()
            conn = SQLConnect.mysql_connect();
            for item in member_id:
                SQLFunctions.add_user(conn, item[1],item[0])
            print("inserted "+str(countInserted)+" users");
            sqlCount = SQLFunctions.getUserCount(conn);
            SQLConnect.mysql_close(conn);
            countInserted = sqlCount;
            print("current users in DB: "+str(sqlCount))
            membersToInsert = [];

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

crawl_ciao()

def test_func():
    one_array = [('hello', 'world')]
    f = open('output.txt','w')
    f.write("%s," %one_array[0][0])
    f.write("%s\n" %one_array[0][1])
    f.close()
#test_func()
