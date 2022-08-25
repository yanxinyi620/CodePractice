import MySQLdb


# 连接mysql，查看数据库列表
serv = MySQLdb.connect(host = "localhost", user = "root", passwd = "12345678")

# 使用cursor()方法获取操作游标
c = serv.cursor()

# 使用execute方法执行SQL语句
c.execute("SHOW DATABASES")

# fetchall() 方法获取数据
r = c.fetchall()
print([i[0] for i in r])

# 关闭mysql连接
serv.close()


# # 连接mysql，查看数据库ppc
db = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='12345678',db='ppc')

cursor = db.cursor()

# 查看版本
cursor.execute('SELECT VERSION()')
data = cursor.fetchone()
print("Database version : %s " % data)

# 查看table
cursor.execute('show tables;')
r = cursor.fetchall()
print([i[0] for i in r])

# 查看数据
cursor.execute('select * from t_job_unit;')
# r = cursor.fetchall()
r = cursor.fetchone()
print(r)

db.close()
