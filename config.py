import os

# 是否开启debug模式
DEBUG = True

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", 'Aa568718')
db_address = os.environ.get(
    "MYSQL_ADDRESS",
    'sh-cynosdbmysql-grp-qj3bw2vq.sql.tencentcdb.com:26882',
)
