import  time
import json
# from urllib import request ,parse
import  requests
import xlrd
import os

from_add ="0x123456789"
private_key = "privatekey"
interface_key = '2018YQTCKEY'

issueStatus = {0:"未创建",1:"已经创建",2:"进行中",3:"成功",4:"失败",5:"已取消"}
MinIssueCoin  =  100000000.0  #最小0.1YOU
HeartbeatxlsFile = 't_heartbeat.xls'
CoinIssueXls =  'coinIssue.xls'

def readissue(row):
    data = xlrd.open_workbook(CoinIssueXls)
    table = data.sheets()[0]
    data_list = []
    data_list.extend(table.row_values(row))

    return data_list[0] ,data_list[1],data_list[2]

def send_coin_url(coinbase,user,you):
   body = {"coinbase":coinbase,"user":user,"you":you,"from_addr":from_add,"private_key":private_key,"interface_key":interface_key}
   url = 'http://localhost:3259/blockchain/youcoin_issue'
   r = requests.post(url, data=body)
   print(r.text)

if __name__ == '__main__':

    path = os.path.dirname(os.path.abspath('__file__'))+"/temp"
    HeartbeatxlsFile = path + "/"+HeartbeatxlsFile
    CoinIssueXls = path + "/"+CoinIssueXls


    data = xlrd.open_workbook(CoinIssueXls)
    table = data.sheets()[0]
    rows = table.nrows

    i=1
    while(i<rows):
        coinbases, user, you = readissue(i)
        print(coinbases,user,you)
        send_coin_url(coinbases, user, int(you))
        i=i+1
        time.sleep(1)
    #


