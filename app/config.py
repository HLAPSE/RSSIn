DEBUG = False
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://hlapse:h91040635!@rm-uf6gm31bj3hm81y14to.mysql.rds.aliyuncs.com/rss' + '?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT
JWT_ERROR_MESSAGE_KEY = "messsage"
JWT_ACCESS_TOKEN_EXPIRES = False

# APScheduler
SCHEDULER_API_ENABLED = True
SCHEDULER_EXECUTORS = {'default': {'type': 'threadpool', 'max_workers': 20}}