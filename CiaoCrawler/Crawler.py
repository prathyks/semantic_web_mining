__author__ = 'admin'
import requests
import sys
import re
import time
import Sql_Connection
import SQLFunction
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
def crawl_product():
    conn = Sql_Connection.mysql_connect()
    SQLFunction.create_prod(conn)
    count=SQLFunction.getUserCount(conn)
    cur1=Sql_Connection.mysql_select_query(conn,'select * from userinfo')
    for x in range(1,count):
        member_id=(cur1.fetchone())
        print("member_id")
        print(member_id[0])
        #member_id = [('richada','5515635')]
        membersToInsert = [];
        #print(1)
        url = 'http://www.ciao.co.uk/member_view.php/MemberId/' + str(member_id[0]) + '/TabId/1'
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
        for_products_rated = 0
        tr_tag = soup_obj.find('tbody')
        # Get the number of reviews
        tr_tag2 = soup_obj.find('tr', {'id':'member_details_opinion_written'})
        #print(tr_tag2)
        try:
            if tr_tag != None:
                num_of_reviews = int(tr_tag2.contents[3].contents[0].split(' ',1)[0])
            else:
                num_of_reviews=0
        except AttributeError as e:
            continue
        print('number of reviews=%d'%num_of_reviews)
        count=0
        link=0
        valid=0
        while num_of_reviews>0:
            for i in tr_tag.find_all('a',href=True):
                try:
                    #print('COUNT =%d'%count)
                    j=i['href']
                    if(valid>1):
                        prod_category=i.text
                        valid=valid-1
                    elif(valid>0):
                        prod_subcategory=i.text
                        print(prod_id,prod_name,prod_category,prod_subcategory)
                        SQLFunction.add_product(conn,prod_id,prod_name,prod_category,prod_subcategory)
                        valid=valid-1
                except:
                    print(sys.exc_info()[0])
                    valid=valid-1
                    print("exception occured")
                    continue
                if(valid==0):
                    count = count+1
                    match = re.search(r'http://.*.ciao.co.uk/.+__\d+', j)
                    if match:
                        valid=2
                        count=count+1
                        str1=str(j)
                        left = str1.split('/')
                        final = left[3].split('__')
                        prod_name=final[0]
                        prod_id=final[1]
                        #print(prod_id + " " +prod_name)

            if num_of_reviews>15:
                link=link+15
                url = 'http://www.ciao.co.uk/member_view.php/MemberId/' + str(member_id[0]) + '/TabId/2/Start/' + str(link)
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
                tr_tag = BeautifulSoup(plain_text)
            num_of_reviews = num_of_reviews - 15

    Sql_Connection.mysql_close(conn)

crawl_product()
