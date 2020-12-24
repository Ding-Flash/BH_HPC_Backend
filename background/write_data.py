import logging

import database
from database.sql import node_history_sql_gen, job_history_sql_gen
from state import all_cluster_state, entire_cluster_state, all_queue_state, entire_queue_state
from state.base_class import QueueStateBase


def write_data_to_mysql():
    logging.debug("将节点及核心信息写入历史数据库")
    _write_node_data()
    logging.debug("将任务及用户信息写入历史数据库")
    _write_job_data()


def _write_node_data():
    sql_value = []
    # 用的是有序字典，因此可以这么使用
    for key, state in all_cluster_state.items():
        if 'other_cluster_state' in key:
            break
        sql_value.append(state.node_total_state.running)
        sql_value.append(state.node_total_state.unavailable)
        sql_value.append(state.node_total_state.total)
        sql_value.append(state.core_total_state.running)
        sql_value.append(state.core_total_state.unavailable)
        sql_value.append(state.core_total_state.total)

    sql_value.append(entire_cluster_state.node_total_state.running)
    sql_value.append(entire_cluster_state.node_total_state.unavailable)
    sql_value.append(entire_cluster_state.node_total_state.total)
    sql_value.append(entire_cluster_state.core_total_state.running)
    sql_value.append(entire_cluster_state.core_total_state.unavailable)
    sql_value.append(entire_cluster_state.core_total_state.total)
    node_history_sql = node_history_sql_gen(*sql_value)
    database.history_hpc_db.execute(node_history_sql)


def _write_job_data():
    sql_value = []
    sql_value.append(entire_queue_state.get_user_waiting_num())
    sql_value.append(entire_queue_state.get_user_running_num())
    sql_value.append(entire_queue_state.get_user_total_num())
    sql_value.append(entire_queue_state.job_running)
    sql_value.append(entire_queue_state.job_waiting)
    sql_value.append(entire_queue_state.job_total)
    # 用的是有序字典
    queue: QueueStateBase
    for key, queue in all_queue_state.items():
        if 'other_queue_state' in key:
            break
        sql_value.append(queue.get_user_waiting_num())
        sql_value.append(queue.get_user_running_num())
        sql_value.append(queue.get_user_total_num())
        sql_value.append(queue.job_running)
        sql_value.append(queue.job_waiting)
        sql_value.append(queue.job_total)
    job_history_sql = job_history_sql_gen(*sql_value)
    database.history_hpc_db.execute(job_history_sql)
