# 初始化数据库
from database.manager import SQLManager
from config import DB_CONFIG

slurm_db = SQLManager(DB_CONFIG["slurm_db"])
history_hpc_db = None
