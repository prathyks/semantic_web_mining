__author__ = 'udayrakesh'

import re

import Sql_Connection
import stop_words
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

cachedWords = stop_words.get_stop_words('english')
def Calculate_similarity(documents):
    for document in documents:
        document = document.lower()
        words = re.findall(r'\w+', document,flags=re.UNICODE | re.LOCALE)
        #print(words)
        important_words = ' '.join(filter(lambda x: x not in cachedWords, words))
        document = important_words
        #print(document)
    tfidf_vectorizer = TfidfVectorizer()
    i=0
    j=0
    docs = [' ',' ']
    final_list = list()
    while i<len(documents):
        j=i+1
        docs[0] = documents[i]
        while j<len(documents):
            docs[1] = documents[j]
            tfidf_matrix = tfidf_vectorizer.fit_transform(docs)
            arr = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
            final_list.append(arr[0][0])
            j+=1
        i+=1
    return final_list

def individual_content_similarity():
    conn = Sql_Connection.mysql_connect()
    cursor = conn.cursor()
    cursor.execute('select user_id,product_id,count(review_id) from review group by user_id,product_id having count(review_id)>1')
    temp = cursor.fetchall()
    Sql_Connection.create_ICS(conn)
    for i in range(0,len(temp)):
        cursor.execute("select review_content from review where user_id = "+str(temp[i][0])+" and product_id = "+str(temp[i][1]))
        list = []
        a = cursor.fetchone()[0]
        b = cursor.fetchone()[0]
        list.append(a);
        list.append(b)
        sim = Calculate_similarity(list)
        print(sim[0])
        cursor.execute('insert into individual_content_similarity values(%d,%d,%f)' % (temp[i][0], temp[i][1], sim[0]))
        cursor.execute('commit')
individual_content_similarity()

