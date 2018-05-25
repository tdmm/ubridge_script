# -*- coding:utf-8 -*-
#!/usr/bin/env python
import  pymysql
import xlrd
from xlutils.copy import copy
import os
import xlwt
from collections2 import OrderedDict

# "t_heartbeat": "CREATE TABLE IF NOT EXISTS " + Schema + ".t_heartbeat (" +
# "`F_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT," +
# "`F_boxid` varchar(128) NOT NULL DEFAULT ''," +
# "`F_binduser` varchar(128) NOT NULL DEFAULT ''," +
# "`F_coinbase` varchar(128) DEFAULT ''," +
# "`F_period` datetime NOT NULL ," +
# "`F_period_type` tinyint(4) DEFAULT '0' COMMENT '0 一天'," +
# "`F_beat` int(10) unsigned DEFAULT '0' COMMENT '心跳次数'," +
# "`F_earn_amount` bigint(20) unsigned DEFAULT '0'," +
# "`F_online` bigint(20) unsigned DEFAULT 0," +
# "`F_create_time` datetime NOT NULL," +
# "`F_modify_time` datetime NOT NULL," +
# "PRIMARY KEY (`F_id`)," +
# "UNIQUE KEY `t_heartbeat_F_boxid_F_coinbase_F_binduser_F_period_uindex` (`F_boxid`,`F_coinbase`,`F_binduser`,`F_period`)" +
# ") ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;",


MinIssueCoin  =  100000000.0  #最小0.1YOU
HeartbeatxlsFile = 't_heartbeat.xls'
CoinIssueXls = 'coinIssue.xls'

def connect_mysql():
    db_config = {
        # 'host': '172.19.160.33',
        # 'port': 8306,
        # 'user': 'root',
        # 'passwd': 'act2141c88154edae3c172',
        # 'db': 'ubridge'
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': '123456',
        'db': 'ubridge'
    }
    c = pymysql.connect(**db_config)
    return c

def DownloadHeartbeatList():

    #download t_heartbeat data
    c = connect_mysql()  # 首先连接数据库
    coursor = c.cursor()
    sql = 'select * from t_heartbeat where F_period <= last_day(date_sub(now(),INTERVAL 1 MONTH)) and  ' \
          'F_period>last_day(date_sub(now(),INTERVAL 2 MONTH));'

    coursor.execute(sql)
    heartbeat_list = coursor.fetchall()
    c.close()

    SaveHeartbeatList(heartbeat_list)
    return heartbeat_list



def CreateHeartbeatXls():
    if os.path.exists(HeartbeatxlsFile) == True:
        print("remove", HeartbeatxlsFile)
        os.remove(HeartbeatxlsFile)

    print("create ", HeartbeatxlsFile)
    xls = xlwt.Workbook(encoding='utf8')
    table = xls.add_sheet("心跳表")
    table.write(0, 0, 'F_id')
    table.write(0, 1, '盒子id')
    table.write(0, 2, '绑定用户')
    table.write(0, 3, '钱包地址')
    table.write(0, 4, "时间")
    table.write(0, 5, "时间类型")
    table.write(0, 6, "心跳次数")
    table.write(0, 7, "收益")
    table.write(0, 8, "在线时长")
    table.write(0, 9, "创建时间")
    table.write(0, 10, "修改时间")
    xls.save(HeartbeatxlsFile)

def CreateIssueXls():
    if os.path.exists(CoinIssueXls) == True:
        print("remove", CoinIssueXls)
        os.remove(CoinIssueXls)

    xls = xlwt.Workbook(encoding='utf8')
    table = xls.add_sheet("代币分发")
    table.write(0, 0, 'coinbase')
    table.write(0, 1, 'user')
    table.write(0, 2, 'you')
    print("create", CoinIssueXls,"\n")
    xls.save(CoinIssueXls)

def SaveIssue(eligibleIssule):
    # 记下需要发币的地址s
    CreateIssueXls()
    xls = xlrd.open_workbook(CoinIssueXls)
    nxls = copy(xls)
    coinsheet = nxls.get_sheet(0)

    index = 0
    for key, value in eligibleIssule.items():
        index = index + 1
        coinsheet.write(index, 0, key[0])   #coinbase
        coinsheet.write(index, 1, key[1])    #user
        coinsheet.write(index, 2, value)    #you

    nxls.save(CoinIssueXls)




def SaveHeartbeatList(heartbeat_list):
    xls = xlrd.open_workbook(HeartbeatxlsFile)
    nxls = copy(xls)
    coinsheet = nxls.get_sheet(0)

    index = 1

    for row in heartbeat_list:
        coinsheet = nxls.get_sheet(0)
        coinsheet.write(index, 0, row[0])
        coinsheet.write(index, 1, row[1])
        coinsheet.write(index, 2, row[2])
        coinsheet.write(index, 3, row[3])
        coinsheet.write(index, 4, str(row[4]))
        coinsheet.write(index, 5, row[5])
        coinsheet.write(index, 6, row[6])
        coinsheet.write(index, 7, str(row[7]))
        coinsheet.write(index, 8, row[8])
        coinsheet.write(index, 9, str(row[9]))
        coinsheet.write(index, 10, str(row[10]))

        index=index+1
        print("save heartbeat,index:",index)

    nxls.save(HeartbeatxlsFile)



def CountEarn(heartbeat_list):
    # 计算每个用户/地址 的发币数
    allIssue = {}
    eligibleIssule = {}
    coinbase_list = []
    user_list = []
    sum = 0
    issue_num = 0

    for row in heartbeat_list:
        coinbase = row[3]
        user = row[2]
        you = int(row[7])
        key = (coinbase, user)

        if allIssue.get(key) == None:
            allIssue[key] = you
        else:
            allIssue[key] += you

        # 去除不适合发的
        ##########################################################################
    user_twice = {}
    coinbase_twice = {}
    too_little = {}

    for key, value in allIssue.items():
        if key[0] in coinbase_list:
            coinbase_twice[key]=value
        if key[1] in user_list:
            user_twice[key] = value
        if value < MinIssueCoin:
            too_little[key] = value
            continue
        else:
            eligibleIssule[key] = value
            issue_num = issue_num + 1
            sum += value

            coinbase_list.append(key[0])
            user_list.append(key[1])


    print('\n\n################################################################################')
    print("\n\n#########User use More than twice")
    for col in user_twice:
        print(col)
    print("\n\n#########Coinbase use more than twice")
    for col in coinbase_twice:
        print(col)
    print("\n\n#########Too little youcoin to send")
    for col in too_little:
        print(col,"     value:",too_little[col])

    print('\n\nsIssue Coin statistics\n')
    print("issue_num:", issue_num, "  sum:", sum)
    if issue_num != 0:
        print("average:", sum / issue_num)

    print('################################################################################')

    # 记下需要发币的地址s
    SaveIssue(eligibleIssule)


if __name__ == '__main__':

    path = os.path.dirname(os.path.abspath('__file__'))+"/temp"
    HeartbeatxlsFile = path + "/"+HeartbeatxlsFile
    CoinIssueXls = path + "/"+CoinIssueXls


    CreateHeartbeatXls()
    heartbeat_list =  DownloadHeartbeatList()

    CountEarn(heartbeat_list)