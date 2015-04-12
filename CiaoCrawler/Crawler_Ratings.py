from setuptools.compat import unicode
from setuptools.compat import unicode

__author__ = 'udayrakesh'

import requests
import sys
import re
import time
import Sql_Connection
import SQLFunctions
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError

def crawl_review():
    conn = Sql_Connection.mysql_connect()
    Sql_Connection.create_review(conn)
    count=SQLFunctions.getUserCount(conn)
    cur1=Sql_Connection.mysql_select_query(conn,'select * from userinfo where id >6889928 and id <=6917773')
    for x in range(1,count):
        member_id=(cur1.fetchone())
        #print('memberid='+str(member_id[0]))
        #member_id = [('richada','5515635')]
        url = 'http://www.ciao.co.uk/member_view.php/MemberId/' + str(member_id[0]) + '/TabId/1'
        #print(url)
        try:
            source_code = requests.get(url)
            time.sleep(2)
        except ConnectionError as e:
            print(e)
        except ConnectionResetError as e:
            print(e)
        plain_text = source_code.text
        #print(plain_text)
        soup_obj = BeautifulSoup(plain_text)
        tr_tag = soup_obj.find('tbody')
        tr_tag2 = soup_obj.find('tr', {'id':'member_details_opinion_written'})
        try:
            if tr_tag != None:
                num_of_reviews = int(tr_tag2.contents[3].contents[0].split(' ',1)[0])
            else:
                num_of_reviews = 0
        except AttributeError as e:
            print(e)
        print('number of reviews=%d'%num_of_reviews)
        count=4
        link=0
        while num_of_reviews > 0:
            for i in tr_tag.find_all('a',href=True):
                try:
                    j = i['href']
                    #print(j)
                    match1 = re.search(r'_Review_', j)
                    if match1:
                        count=0
                        #print(j)
                        reviewid_initial = str(j).split('_Review_')
                        review_ID = reviewid_initial[1]
                        #print(review_ID)
                        source_code1 = requests.get(j)
                        plain_text1 = source_code1.text
                        soup_obj1 = BeautifulSoup(plain_text1)
                        #print(soup_obj1.contents)
                        tr_tag1 = str(soup_obj1.find('title'))
                        rname_first = tr_tag1.split('-')
                        review_name = rname_first[2].split('</title>')
                        review_name=review_name[0].encode('ascii','ignore').decode('ascii')
                        #print(review_name[0])
                        temp=soup_obj1.find('span',{'class':'m-reer-ddwrap'})
                        review_date = temp.contents[1].contents[1].get('content')
                        #print(review_date)
                        tmp_rating=soup_obj1.find('span',{'class':'e-reer-ustars'})
                        review_rating = tmp_rating.contents[1].get('alt')
                        #print(review_rating)
                        tmp = soup_obj1.find_all('div',{'class':'reviewText'})
                        review_content = tmp[0].find('p').text
                        # try:
                        #     unicode(review_content, "ascii")
                        # except UnicodeError:
                        #     review_content = unicode(review_content, "utf-8")
                        review_content = review_content.replace("'","''")
                        review_content = review_content.encode('ascii', 'ignore').decode('ascii')
                    else:
                        match = re.search(r'http://.*.ciao.co.uk/.+__\d+', j)
                        if match and count == 0:
                            str1 = str(j)
                            left = str1.split('/')
                            final = left[3].split('__')
                            prod_id=final[1]
                            count += 1
                            #print("product id="+prod_id)
                            print(review_ID + review_name +' '+review_date + ' ' +review_rating +' ' +prod_id +' ' + str(member_id[0]))
                            Sql_Connection.add_review(conn,review_ID,review_name,review_rating,review_date,review_content,prod_id,str(member_id[0]))
                except:
                    print('Exception occured')
                    num_of_reviews -= 1
                    print(sys.exc_info())
                    pass
            if num_of_reviews > 15:
                link = link + 15
                url = 'http://www.ciao.co.uk/member_view.php/MemberId/' + str(member_id[0]) + '/TabId/1/Start/' + str(link)
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











crawl_review()


