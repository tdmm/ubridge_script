
import  time
import json
# from urllib import request ,parse
import  requests
import xlrd
import  pymysql
import sys
import os
import random
import time



sql1 = "INSERT INTO `ubridge`.`t_heartbeat` (`F_boxid`, `F_binduser`, `F_coinbase`, `F_period`, `F_period_type`, `F_beat`, `F_earn_amount`, `F_online`, `F_create_time`, `F_modify_time`) VALUES "
sql2 = "('233', '23', '323', '2018-05-22 00:00:00', '2', '2', '2', '3', '2018-05-22 00:00:00', '2018-05-22 00:00:00');"

HeartbeatxlsFile = '/Users/phoenix/go/src/ubox.ubridge/coin_issue/t_heartbeat.txt'
SendYouXlsFile = '/Users/phoenix/go/src/ubox.ubridge/coin_issue/SendYou.txt'


userlist = []
coinbaselist =[]
boxidlist = []
num =0

def connect_mysql():
    db_config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': '123456',
        'db': 'ubridge'
    }
    c = pymysql.connect(**db_config)
    return c

def create_col():
    i =1000
    while i>0:
        i=i-1
        userlist.append("user"+str(i))

    j = 10000
    while j>0:
        j = j -1
        coinbaselist.append("coinbase"+str(j))

    k = 10000
    while k >0:
        k = k -1
        boxidlist.append("boxid"+str(k))




def create_heartbeat(db,F_boxid,F_binduser,F_coinbase,F_period,F_period_type,F_beat,F_earn_amount,F_online,F_create_time,F_modify_time):
    sql2 = "('"+F_boxid+"','"+F_binduser+"','"+F_coinbase+"','"+F_period+"',"+F_period_type+","+F_beat+","+\
           F_earn_amount+","+F_online+",'"+F_create_time+"','"+F_modify_time+"');"

    # print(sql1 + sql2)


    coursor = db.cursor()

    try:
        # 执行sql语句
        coursor.execute(sql1 + sql2)
        # 提交到数据库执行
        db.commit()
        print("success:"+F_boxid+F_binduser+F_coinbase)
    except:
        # Rollback in case there is any error
        db.rollback()
        print("failed:" + F_boxid + F_binduser + F_coinbase)

    # time.sleep(0.01)


if __name__ == '__main__':
    # create_heartbeat("boxi01","user01","coinbase01","2018:01:02 00:00:00","0","10000","100000","100000",
    #                  "2018:01:02 00:00:00","2018:01:02 00:00:00")
    create_col()

    timestr= "2018-04-22 00:00:00"

    db = connect_mysql()  # 首先连接数据库

    i =30000
    while i>0:
        i = i -1

        earn = str(random.randint(0, 18446744073709551615))
        online = str(random.randint(0, 18446744073709551615))
        user = random.sample(userlist, 1)[0]
        boxid = random.sample(boxidlist, 1)[0]  # 从list中随机获取5个元素，作为一个片断返回
        coibase = random.sample(coinbaselist, 1)[0]
        create_heartbeat(db,boxid,user,coibase,timestr,"0","1111",earn,online,timestr,timestr)

    db.close()



