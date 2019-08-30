# -*- coding:utf-8 -*-

import MySQLdb

db = MySQLdb.connect("localhost","root","962424lgj","test",charset='utf8')

cursor = db.cursor()
# SQL 插入语句
sql = "INSERT INTO test(item,status,pub_date) VALUES(ie,er,NOW());"
try:
   # 执行sql语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# 关闭数据库连接
db.close()
