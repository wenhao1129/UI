# coding=UTF-8
from PyQt5.QtWidgets import QMainWindow
import os
import time
import shutil
import pymysql
from timeit import default_timer

# 定义保存外部程序生成logfile
host = 'lwh'
port = 3306
db = 'mysql_test'
user = 'mysql_test'
password = 'mysql_test'
# ---- 用pymysql 操作数据库
conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
'''插入单条数据'''
#打开数据库连接，不指定数据库
conn.select_db('pythondb')

cur=conn.cursor()#获取游标

#创建user表
cur.execute('drop table if exists user')
sql="""CREATE TABLE IF NOT EXISTS `test_information` (
      `Model_Name` int(11) NOT NULL,
      `MO_Number` int(16) NOT NULL,
      `station_Name` int(7) NOT NULL,
      `Robot_SN` int(6) NOT NULL,
      `Tester_Name` NOT NULL,
      `Error_Code` NOT NULL,
      `Test_Result` NOT NULL,
      PRIMARY KEY (`Robot_SN`)
    ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""

cur.execute(sql)

insert=cur.execute("insert into user values(1,'tom',18)")
print('添加语句受影响的行数：', insert)

#另一种插入数据的方式，通过字符串传入值
sql="insert into user values(%s,%s,%s)"
cur.execute(sql,(3,'kongsh',20))

cur.close()
conn.commit()
conn.close()
print('sql执行成功')
