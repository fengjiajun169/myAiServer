import os

# 是否开启debug模式
DEBUG = True

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", 'Fjj111111!')
db_address = os.environ.get("MYSQL_ADDRESS", '10.3.108.152:3306')
chat_api_key = os.environ.get("CHAT_API_KEY", '0')
speech_key = os.environ.get("SPEECH_KEY", '0')
service_region = os.environ.get("SERVICE_REGION", '0')
# username = 'root'
# password = 'Fjj111111!'
# db_address = '10.3.108.152:3306'
