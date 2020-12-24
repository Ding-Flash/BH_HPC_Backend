"""
定义后端程序运行信息
"""

HOST = "10.111.3.80"
PORT = 9000
# 数据更新时间，单位 秒，数据库更新为每5分钟一次，低于5分钟浪费资源
UPDATE_INTERVAL = 300

"""
定义mysql相关配置信息
"""
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "passwd": "Networkliyunchunandliwei2021$",
    "charset": "utf8",

    "slurm_db": "hpc",  # 用于存储从slurm中拿出的job node信息的库
    "job_table": "job_5min",
    "node_table": "node_5min",

    "history_hpc_db": "hpc_history",  # 用于存储所有历史信息的库
    "history_node_table": "node_history",
    "history_queue_table": "queue_history"
}

"""
定义程序日志输出信息
"""
# 日志文件路径，输入绝对路径
LOG_DIR = '/home/hpcdev/HPC/HPC_Backend/logs'
# 日志输出格式配置
LOG_CONFIG_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(threadName)s:%(thread)d %(levelname)s : %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': "DEBUG",
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'maxBytes': 1048576000,
            'backupCount': 20,
            'encoding': 'utf8',
            'filename': LOG_DIR + '/hpc_backend.log',
            'mode': 'w+'
        },
    },
    'root': {
        'handlers': ['console', 'file_handler'],
        'level': 'DEBUG',
        'propagate': False
    }
}
