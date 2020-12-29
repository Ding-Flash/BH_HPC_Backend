import heapq
import logging

import database
import state
from config import DB_CONFIG

time_format = "%Y-%m-%d %H:%M:%S"


def get_job_list():
    return [{**job.to_dict(), 'key': hash(job)} for job in state.job_state_list]


def get_node_list():
    return [{**node.to_dict(), 'key': hash(node)} for node in state.node_state_list]


def get_job_wait_top(top_num):
    wait_job_list = []
    for job in state.job_state_list:
        if 'PENDING'.lower() in job.state.lower():
            wait_job_list.append(job)
    return {
        'wait_job_topk': [{'job_name': job.job_name, 'time': job.get_time_delta_sec()} for job in
                          heapq.nlargest(top_num, wait_job_list,
                                         key=lambda x: x.get_time_delta_sec())],
    }


def get_job_run_top(top_num):
    run_job_list = []
    for job in state.job_state_list:
        if 'RUNNING'.lower() in job.state.lower():
            run_job_list.append(job)

    return {
        'wait_job_topk': [{'job_name': job.job_name, 'time': job.get_time_delta_sec()} for job in
                          heapq.nlargest(top_num, run_job_list,
                                         key=lambda x: x.get_time_delta_sec())],
    }


def get_node_data(date_from, date_to):
    return_data_dict = {
        'info': [],
        'stat': {}
    }
    try:
        node_res = database.history_hpc_db.get_list(
            f"select * from {DB_CONFIG['history_node_table']} where record_time between '{date_from}' and '{date_to}'")

        stat_pec_data = {
            'cpu': {
                'node': {
                    'max': 0.0,
                    'min': 1000.0,
                    'avg': 0.0
                },
                'core': {
                    'max': 0.0,
                    'min': 1000.0,
                    'avg': 0.0
                }
            },
            'gpu': {
                'node': {
                    'max': 0.0,
                    'min': 1000.0,
                    'avg': 0.0
                },
                'core': {
                    'max': 0.0,
                    'min': 1000.0,
                    'avg': 0.0
                }
            },
            'all': {
                'node': {
                    'max': 0.0,
                    'min': 1000.0,
                    'avg': 0.0
                },
                'core': {
                    'max': 0.0,
                    'min': 1000.0,
                    'avg': 0.0
                }
            }
        }

        for node_info in node_res:
            return_data = {
                'time': node_info['record_time'].strftime(time_format),
                'cpu_running_node_pec': node_info['cpu_running_node'] / node_info['cpu_total_node'],
                'cpu_running_core_pec': node_info['cpu_running_core'] / node_info['cpu_total_core'],
                'gpu_running_node_pec': node_info['gpu_running_node'] / node_info['gpu_total_node'],
                'gpu_running_core_pec': node_info['gpu_running_core'] / node_info['gpu_total_core'],
                'all_running_node_pec': node_info['running_node'] / node_info['total_node'],
                'all_running_core_pec': node_info['running_core'] / node_info['total_core']
            }
            # 将当前节点信息加入准备返回的数据表中
            return_data_dict['info'].append(return_data)
            # 计算cpu集群的节点、核心统计信息
            compute_node_stat_data('cpu', return_data, stat_pec_data)
            # 计算gpu集群的节点、核心统计信息
            compute_node_stat_data('gpu', return_data, stat_pec_data)
            # 计算集群总体的节点、核心统计信息
            compute_node_stat_data('all', return_data, stat_pec_data)

        # 计算平均值
        stat_pec_data['cpu']['node']['avg'] = stat_pec_data['cpu']['node']['avg'] / len(
            return_data_dict['info'])
        stat_pec_data['cpu']['core']['avg'] = stat_pec_data['cpu']['core']['avg'] / len(
            return_data_dict['info'])

        stat_pec_data['gpu']['node']['avg'] = stat_pec_data['gpu']['node']['avg'] / len(
            return_data_dict['info'])
        stat_pec_data['gpu']['core']['avg'] = stat_pec_data['gpu']['core']['avg'] / len(
            return_data_dict['info'])

        stat_pec_data['all']['node']['avg'] = stat_pec_data['all']['node']['avg'] / len(
            return_data_dict['info'])
        stat_pec_data['all']['core']['avg'] = stat_pec_data['all']['core']['avg'] / len(
            return_data_dict['info'])

        return_data_dict['stat'] = stat_pec_data
        return return_data_dict
    except Exception as e:
        logging.exception(e)
        return return_data_dict


def compute_node_stat_data(cluster_type, return_data, stat_pec_data):
    if return_data[cluster_type + '_running_node_pec'] > stat_pec_data[cluster_type]['node']['max']:
        stat_pec_data[cluster_type]['node']['max'] = return_data[cluster_type + '_running_node_pec']
    if return_data[cluster_type + '_running_node_pec'] < stat_pec_data[cluster_type]['node']['min']:
        stat_pec_data[cluster_type]['node']['min'] = return_data[cluster_type + '_running_node_pec']
    stat_pec_data[cluster_type]['node']['avg'] += return_data[cluster_type + '_running_node_pec']

    if return_data[cluster_type + '_running_core_pec'] > stat_pec_data[cluster_type]['core']['max']:
        stat_pec_data[cluster_type]['core']['max'] = return_data[cluster_type + '_running_core_pec']
    if return_data[cluster_type + '_running_core_pec'] < stat_pec_data[cluster_type]['core']['min']:
        stat_pec_data[cluster_type]['core']['min'] = return_data[cluster_type + '_running_core_pec']
    stat_pec_data[cluster_type]['core']['avg'] += return_data[cluster_type + '_running_core_pec']


def get_queue_data(date_from, date_to):
    return_data_dict = {
        'info': [],
        'stat': {}
    }
    try:
        job_res = database.history_hpc_db.get_list(
            f"select * from {DB_CONFIG['history_queue_table']} where record_time between '{date_from}' and '{date_to}'")

        stat_pec_data = {
            'cpu': {
                'job': {
                    'total': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    },
                    'waiting': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    },
                    'running': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    }
                },
                'user': {
                    'total': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    },
                    'waiting': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    },
                    'running': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    }
                }
            },
            'gpu': {
                'job': {
                    'total': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    },
                    'waiting': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    },
                    'running': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    }
                },
                'user': {
                    'total': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    },
                    'waiting': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    },
                    'running': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    }
                }
            },
            'all': {
                'job': {
                    'total': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    },
                    'waiting': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    },
                    'running': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    }
                },
                'user': {
                    'total': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    },
                    'waiting': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    },
                    'running': {
                        'max': 0.0,
                        'min': 1000.0,
                        'avg': 0.0
                    }
                }
            }
        }

        for job_info in job_res:
            return_data = {**job_info,
                           'time': job_info['record_time'].strftime(time_format),
                           }
            return_data_dict['info'].append(return_data)
            # 计算cpu集群的任务、用户数量统计信息
            compute_queue_stat_data('cpu', return_data, stat_pec_data)
            # 计算gpu集群的任务、用户数量统计信息
            compute_queue_stat_data('gpu', return_data, stat_pec_data)
            # 计算集群总体的任务、用户数量统计信息
            compute_queue_stat_data('all', return_data, stat_pec_data)
        # 计算平均值
        compute_queue_stat_avg_data('cpu', stat_pec_data, len(return_data_dict['info']))
        compute_queue_stat_avg_data('gpu', stat_pec_data, len(return_data_dict['info']))
        compute_queue_stat_avg_data('all', stat_pec_data, len(return_data_dict['info']))

        return_data_dict['stat'] = stat_pec_data
        return return_data_dict
    except Exception as e:
        logging.exception(e)
        return return_data_dict


def compute_queue_stat_avg_data(cluster_type, stat_pec_data, num):
    stat_pec_data[cluster_type]['job']['total']['avg'] = \
        stat_pec_data[cluster_type]['job']['total']['avg'] / num
    stat_pec_data[cluster_type]['job']['running']['avg'] = \
        stat_pec_data[cluster_type]['job']['running']['avg'] / num
    stat_pec_data[cluster_type]['job']['waiting']['avg'] = \
        stat_pec_data[cluster_type]['job']['waiting']['avg'] / num

    stat_pec_data[cluster_type]['user']['total']['avg'] = \
        stat_pec_data[cluster_type]['user']['total']['avg'] / num
    stat_pec_data[cluster_type]['user']['running']['avg'] = \
        stat_pec_data[cluster_type]['user']['running']['avg'] / num
    stat_pec_data[cluster_type]['user']['waiting']['avg'] = \
        stat_pec_data[cluster_type]['user']['waiting']['avg'] / num


def compute_queue_stat_data(cluster_type, return_data, stat_pec_data):
    """
    用来计算队列中的任务的一些统计信息
    当前查询时间范围内:   CPU集群最大作业数量、最小作业数量、平均作业数量
                        GPU集群的最大作业数量、最小作业数量、平均作业数量
                        集群总体的最大作业数量、最小作业数量、平均作业数量

                        CPU集群提交作业的最大用户数量、最小用户数量、平均用户数量
                        GPU集群提交作业的最大用户数量、最小用户数量、平均用户数量
                        集群总体提交作业的最大用户数量、最小用户数量、平均用户数量
    :param cluster_type: 集群的类型['cpu','gpu','all']
    :param return_data: 从数据库中查询出来的数据，以字典形式传入
    :param stat_pec_data: 用来保存这些统计信息的字典
    """
    # 计算集群中用户相关的统计信息
    compute_queue_stat_user_or_job_data(cluster_type, 'user', return_data, stat_pec_data)
    # 计算集群中任务相关的统计信息
    compute_queue_stat_user_or_job_data(cluster_type, 'job', return_data, stat_pec_data)


def compute_queue_stat_user_or_job_data(cluster_type, data_type, return_data, stat_pec_data):
    """

    :param cluster_type: 与compute_queue_stat_data函数中相同
    :param data_type: ['user','job'],用来指定计算用户的统计信息还是任务的统计信息
    :param return_data: 与compute_queue_stat_data函数中相同
    :param stat_pec_data: 与compute_queue_stat_data函数中相同
    """
    # 总计
    compute_state_stat_diff_type_data(cluster_type, 'total', data_type, return_data, stat_pec_data)
    # 等待
    compute_state_stat_diff_type_data(cluster_type, 'waiting', data_type, return_data,
                                      stat_pec_data)
    # 运行
    compute_state_stat_diff_type_data(cluster_type, 'running', data_type, return_data,
                                      stat_pec_data)


def compute_state_stat_diff_type_data(cluster_type, state_type, data_type, return_data,
                                      stat_pec_data):
    """

    :param cluster_type: 与compute_queue_stat_data函数中相同
    :param state_type: ['total','waiting','running'],用来指定不同状态的任务或用户的统计信息
    :param data_type: 与compute_queue_stat_user_or_job_data函数中相同
    :param return_data: 与compute_queue_stat_data函数中相同
    :param stat_pec_data: 与compute_queue_stat_data函数中相同
    """
    sql_data_key = cluster_type + '_' + state_type + '_' + data_type
    if return_data[sql_data_key] > stat_pec_data[cluster_type][data_type][state_type]['max']:
        stat_pec_data[cluster_type][data_type][state_type]['max'] = return_data[sql_data_key]
    if return_data[sql_data_key] < stat_pec_data[cluster_type][data_type][state_type]['min']:
        stat_pec_data[cluster_type][data_type][state_type]['min'] = return_data[sql_data_key]
    stat_pec_data[cluster_type][data_type][state_type]['avg'] += return_data[sql_data_key]
