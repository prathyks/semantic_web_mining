import pymysql
import SQLConnect
import SQLFunctions
import datetime
pymysql.install_as_MySQLdb()

def get_groups(conn):
    query = "SELECT group_id,supcount FROM itemsets WHERE pos >=3 GROUP BY group_id"
    cur = SQLConnect.mysql_select_query(conn, query)
    res = cur.fetchall()
    cur.close()
    return res


def list_to_csv(list_u):
    res = ""
    for item in list_u:
        if res == "":
            res = str(item)
        else:
            res += ","+str(item)
    return res


def tupletolist(arr):
    final_list = list()
    for item in arr:
        final_list.append(item[0])
    return final_list


def get_group_members(conn, gid):
    query = "select user_id from itemsets where group_id="+str(gid)+" order by pos"
    cur = SQLConnect.mysql_select_query(conn, query)
    user_list = list()
    res = cur.fetchall()
    for item in res:
        user_list.append(item[0])
    cur.close()
    return user_list

conn = SQLConnect.mysql_connect()
result = get_groups(conn)
IMC_file = open('IMC.txt','w')
for record in result:
    group_id = record[0]
    supcount = record[1]
    #print(group_id)
    users = get_group_members(conn, group_id)
    common_prods = list()
    c1 = tupletolist(SQLFunctions.get_products_of_given_userid(conn, str(users[0])))
    for user in users[1:]:
        c2 = tupletolist(SQLFunctions.get_products_of_given_userid(conn, str(user)))
        common_prods = [val for val in c1 if val in c2]
        c1 = common_prods
    user_csv = list_to_csv(users)
    print(common_prods)
    print(user_csv)
    num_prods = len(common_prods)
    imc = dict()
    for user in users:
        imc[user] = 0
    for prod_id in common_prods:
        query = "select user_id, review_date from review where product_id="+str(prod_id)+" AND\
        user_id in ("+str(user_csv)+") group by user_id"
        cur = SQLConnect.mysql_select_query(conn, query)
        datearray = list()
        user_date_dict = dict()
        num_users = len(users)
        for item in cur:
            user_date_dict[item[0]] = int(item[1].strftime("%s"))
            datearray.append(int(item[1].strftime("%s")))
        first_date = min(datearray)
        last_date = max(datearray)
        diff = last_date - first_date
        user_avg_gm = dict()
        sum_dates = sum(datearray)
        for item in user_date_dict.items():
            temp = 0
            curr = item[0]
            temp_sum = 0
            for temp_item in user_date_dict.items():
                if temp_item[0] != curr:
                    temp_sum += (temp_item[1] - first_date)
            temp = temp_sum / (num_users-1)
            user_avg_gm[item[0]] = temp
        for user in users:
            imc[user] += (abs(user_date_dict[user] - first_date - user_avg_gm[user]) / diff)
    for k, v in imc.items():
        imc[k] = v / num_prods
    pos = 1
    imc_arr = list()
    for user in users:
        imc_arr.append(imc[user])
    IMC_file.write("%s #IMC: %s\n" % (users, imc_arr))
    # for user in users:
    #     #SQLFunctions.add_imc(conn, group_id, pos, user, supcount, imc[user])
    #     pos += 1
IMC_file.close()





















