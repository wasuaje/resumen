import MySQLdb
db=MySQLdb.connect(host='10.3.0.130',user='root',passwd='root',db='mysql')
cursor=db.cursor()
sql='SELECT host,user,password FROM user;'
cursor.execute(sql)
resultado=cursor.fetchall()
for registro in resultado:
    print registro[0] , '|' , registro[1]

