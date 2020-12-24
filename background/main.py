import logging
import pytz
from apscheduler.schedulers.background import BackgroundScheduler

from background.update import update_job_state, update_node_state, update_cluster_state, clear_state
from background.write_data import write_data_to_mysql
from common.utils import print_placeholder
from config import UPDATE_INTERVAL, DB_CONFIG
from database import slurm_db
import state

background_main_program = BackgroundScheduler(timezone=pytz.timezone('Asia/Shanghai'))


@background_main_program.scheduled_job('interval', seconds=UPDATE_INTERVAL)
def update_state():
    logging.info('执行数据更新')
    # 获取数据来定期更新内存中的状态
    # 获取任务队列信息
    job_list = slurm_db.get_list('select * from ' + DB_CONFIG['job_table'])
    # 获取节点列表信息
    node_list = slurm_db.get_list('select * from ' + DB_CONFIG['node_table'])

    # 更新状态前需要先清空
    clear_state()
    # 更新节点及核心状态信息
    update_node_state(node_list)
    # 更新用户及任务状态信息
    update_job_state(job_list)
    # 更新集群汇总信息
    update_cluster_state()

    print_placeholder('DEBUG')
    logging.debug(state.all_cluster_state['cpu_cluster_state'].to_dict())
    logging.debug(state.all_cluster_state['gpu_cluster_state'].to_dict())
    logging.debug(state.all_cluster_state['other_cluster_state'].to_dict())

    logging.debug(state.entire_cluster_state.to_dict())

    logging.debug(state.all_queue_state['cpu_queue_state'].to_dict())
    logging.debug(state.all_queue_state['gpu_queue_state'].to_dict())
    logging.debug(state.all_queue_state['other_queue_state'].to_dict())

    logging.debug(state.entire_queue_state.to_dict())
    print_placeholder('DEBUG')

    # 将更新后的状态写入数据库
    write_data_to_mysql()
