import pymysql
import configparser
import datetime
cfp = configparser.ConfigParser()
cfp.read('DBcnf.ini')
config = cfp.items('DB')
print(config)
host = cfp.get('DB', 'host')
username = cfp.get('DB', 'username')
password = cfp.get('DB', 'password')
database = cfp.get('DB', 'database')
tablename = cfp.get('DB','tablename')
expiration = cfp.get('spider','expiration')


today = datetime.date.today()
seven_days_before = today - datetime.timedelta(days=int(expiration))
today = today.strftime("%Y-%m-%d")
seven_days_before = seven_days_before.strftime("%Y-%m-%d")
db = pymysql.connect(host , username, password, database)

cursor = db.cursor()

def createCheckedTable():
    global cursor

    cursor.execute("create table if not exists "+tablename+"("
                   "id int auto_increment  PRIMARY KEY,"
                   "host varchar(255),"
                   "checked_date date ,"
                   "rspcode varchar(3),"
                   "rspbody tinyint"
                   ")")

    return True


def insertCheckedHost(host,rspcode,is_None):
    global cursor
    sql = "insert into "+tablename+"(host,rspcode,checked_date,rspbody) values(%s,%s,%s,%s)"
    effectlines = cursor.execute(sql, (host,rspcode,today,is_None))
    print(("effectlines:" + str(effectlines)))
    db.commit()
    return True
def selectWeekHosts():
    print((today,seven_days_before))
    sql = "select domain from "+tablename+" where check_negative_times<=0 and latest_positive_time>"+seven_days_before
    cursor.execute(sql)
    hosts = cursor.fetchall()
    print(hosts)
    return hosts
if __name__ == '__main__':
    #createCheckedTable()
    # insertCheckedHost("www.baidu.com","400")
    hosts = selectWeekHosts()
    for host in hosts:
        print((host[0]))