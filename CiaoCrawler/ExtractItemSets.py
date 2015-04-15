__author__ = 'porus'

## NOTES For my Ref::
####################### Extract review content from the user id's ################
## Take each group, for each user pair in group calculate the similarity of their reviews i.e
## 1.) Collect all products that they reviewed in common.
## 2.) Collect all their reviews for each product.
## 3.) For each product reviews check similarity.
## 4.) Take average of the similarity.
## 5.) Take max of all the averages of all products. This is the output of GCS(g) --> A normalized value.



from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#from nltk.corpus import stopwords
#import pymysql
#import numpy
import stop_words
import re
import SQLConnect
import SQLFunctions
import string


def tupletolist(arr):
    final_list = list()
    for item in arr:
        final_list.append(item[0])
    return final_list

################## Content Similarity #################

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
    return  final_list


grp_grt_sup_2 = list()
grp_grt_2 = list()

############# Find just groups with members greater than 3
with open('../ItemSets/ciao_output_sup4','r') as f:
    i=0
    for line in f:
        i+=1
        #print(line)
        items = line.split(' ')
        items.remove('#SUP:')
        if len(items) > 3:
            items[len(items) - 1] = items[len(items) - 1].split('\n')[0]
            grp_grt_sup_2.append(items)
            grp_grt_2.append(items[0:len(items)-1])
        #print(items)


conn = SQLConnect.mysql_connect()
GCS_file = open('Final_GCS_2.txt','w')

for each_group in grp_grt_2:
    #print(grp_grt_sup_2[0])
    common_prods = list()
    c1 = tupletolist(SQLFunctions.get_products_of_given_userid(conn,each_group[0]))
    ## Find Common Products reviewed by group..
    for user in each_group[1:]:
        c2 = tupletolist(SQLFunctions.get_products_of_given_userid(conn,user))
        common_prods = [val for val in c1 if val in c2]
        c1 = common_prods
    print(len(common_prods))
    ## Now Implement the Formula. GCS(g)
    avg_CS = list()
    for prod in common_prods:
        reviews_for_prod = list()
        for user in each_group:
            #Write a query to fetch reviews by this user on this product. Assuming that a user gave only 1 review to one product.
            x = tupletolist(SQLFunctions.get_reviews_of_given_user_product(conn,user,str(prod)))
            x = str(x[0]).translate(string.maketrans("",""),string.punctuation)
            reviews_for_prod.append(x)
        #print(reviews_for_prod)
        #Now find similarity of these reviews and them calculate average!
        similarity_arr = Calculate_similarity(reviews_for_prod)
        avg_CS.append(sum(similarity_arr)/len(similarity_arr))
    #print(max(avg_CS))
    GCS_file.write("%s #GCS: %s\n" %(each_group,max(avg_CS)))
GCS_file.close()



