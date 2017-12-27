import pymysql
connect=pymysql.Connect(port=3306,user='root',passwd='123456',db='test',charset='utf8')
sql='select * from Student'
cursor=connect.cursor()
cursor.execute(sql)
for row in cursor:
  print(row)
