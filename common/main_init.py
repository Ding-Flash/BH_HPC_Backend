"""
该文件用来进行主程序初始化
"""
import logging
import logging.config
import os
import shutil
import sys

import database
from background.main import background_main_program
from config import LOG_DIR, DB_CONFIG, LOG_CONFIG_DICT
from database import slurm_db, SQLManager
from database.sql import node_history_table_sql, job_history_table_sql


def main_program_init():
    #####################################################################################
    # 日志配置初始化
    #####################################################################################
    # 重新创建日志路径
    shutil.rmtree(LOG_DIR)
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.config.dictConfig(LOG_CONFIG_DICT)
    # 关闭后台调度程序日志
    logging.getLogger('apscheduler').setLevel(logging.ERROR)

    #####################################################################################
    # 检查数据库情况
    #####################################################################################
    # 先检查Slurm信息数据库
    try:
        slurm_db.get_one('select * from ' + DB_CONFIG['job_table'])
        slurm_db.get_one('select * from ' + DB_CONFIG['node_table'])
    except Exception as e:
        logging.exception(e)
        logging.error('Slurm数据库可能缺少数据表，请先进行数据库初始化')
        sys.exit(-1)
    # 再检查history数据库情况
    try:
        # 先检查数据库是否存在
        database.history_hpc_db = SQLManager(DB_CONFIG["history_hpc_db"])
    except Exception as e:
        logging.info(f'创建数据库: {DB_CONFIG["history_hpc_db"]}')
        slurm_db.execute(f'create database {DB_CONFIG["history_hpc_db"]}')
        database.history_hpc_db = SQLManager(DB_CONFIG["history_hpc_db"])
        logging.info(f'数据库 {DB_CONFIG["history_hpc_db"]} 创建成功!')
    try:
        # 再检查数据表是否存在
        database.history_hpc_db.get_one('select * from ' + DB_CONFIG['history_node_table'])
        database.history_hpc_db.get_one('select * from ' + DB_CONFIG['history_queue_table'])
    except Exception as e:
        logging.info(f'创建数据表{DB_CONFIG["history_hpc_db"]}.{DB_CONFIG["history_node_table"]}')
        database.history_hpc_db.execute(node_history_table_sql)
        logging.info(f'创建数据表{DB_CONFIG["history_hpc_db"]}.{DB_CONFIG["history_queue_table"]}')
        database.history_hpc_db.execute(job_history_table_sql)

    #####################################################################################
    # 开启后台程序，更新程序所需状态
    #####################################################################################
    logging.info(f'开启后台程序,自动更新数据状态')
    background_main_program.start()
