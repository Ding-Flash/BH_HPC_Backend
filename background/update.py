# 直接导入包名，然后通过 state.变量名 的方式获取的变量，可以修改变量中的内容，通过from import修改不了
import logging

import state
from state.job_state import JobState
from state.node_state import NodeState


def clear_state():
    """
    在更新状态前需要清空所有状态，并完成相关初始化
    """
    # 清空任务接节点状态
    state.job_state_list.clear()
    state.node_state_list.clear()
    # 清空集群状态信息
    state.entire_cluster_state.clear()
    # 清空任务队列信息
    state.entire_queue_state.clear()


def update_job_state(job_list):
    """
    更新内存中的任务状态
    :param job_list: 从数据库中获取的任务列表
    """
    logging.info("更新任务及用户状态")
    for job_info in job_list:
        state.job_state_list.append(JobState(
            job_info['job_name'],
            job_info['account'],
            job_info['user'],
            job_info['partit'],
            job_info['qos'],
            job_info['num_node'],
            job_info['num_core'],
            job_info['state'],
            job_info['time'],
            job_info['des']
        ))


def update_node_state(node_list):
    """
    更新内存中的节点状态
    :param node_list: 从数据库中获取的节点列表
    """
    logging.info("更新节点及核心状态")
    for node_info in node_list:
        state.node_state_list.append(NodeState(
            node_info['node'],
            node_info['node_state'],
            node_info['all_core'],
            node_info['used_core'],
            node_info['free_core'],
            node_info['cpu_load'],
            node_info['memory'],
            node_info['free_memory'],
            _get_node_type(node_info['node'])
        ))


def update_cluster_state():
    """
    遍历节点列表，根据节点类型不同分别对CPU集群、GPU集群和其他集群中的节点数量状态进行更新
    """
    logging.info("更新汇总信息")
    for node in state.node_state_list:
        # 如果节点类型是GPU
        if node.node_type == "gpu":
            _update_specific_cluster_state(node, "gpu_cluster_state")
        # 如果节点类型是CPU
        elif node.node_type == "cpu":
            _update_specific_cluster_state(node, "cpu_cluster_state")
        # 如果是其他类型节点
        else:
            _update_specific_cluster_state(node, "other_cluster_state")
    # 更新整个集群的状态，将CPU与GPU的核心及节点数累加
    state.entire_cluster_state.update_state()

    # 更新任务队列状态
    for job in state.job_state_list:
        # 如果任务类型是GPU
        if 'gpu'.lower() in job.partition.lower():
            _update_specific_queue_state(job, "gpu_queue_state")
        elif 'cpu'.lower() in job.partition.lower():
            _update_specific_queue_state(job, "cpu_queue_state")
        else:
            _update_specific_queue_state(job, "other_queue_state")
    # 将不同队列中的任务相加获取累积状态
    state.entire_queue_state.update_state()


def _update_specific_queue_state(job, queue_type):
    """
    更新具体的队列状态中的任务、用户信息
    :type queue_type: ["gpu_queue_state","cpu_queue_state","other_queue_state"]
    :type job: JobState
    """
    state.all_queue_state[queue_type].job_total += 1
    state.all_queue_state[queue_type].user_total.add(job.user)
    # 更新任务状态信息
    if "RUNNING".lower() in job.state.lower():
        state.all_queue_state[queue_type].job_running += 1
        state.all_queue_state[queue_type].user_running.add(job.user)
    elif "PENDING".lower() in job.state.lower():
        state.all_queue_state[queue_type].job_waiting += 1
        state.all_queue_state[queue_type].user_waiting.add(job.user)


def _update_specific_cluster_state(node, cluster_type):
    """
    根据节点的状态来更新集群中的节点及核心状态信息
    :param node:NodeState,节点状态
    :param cluster_type: 需要更新状态的集群的类型
    """
    # 更新集群节点相关状态
    state.all_cluster_state[cluster_type].node_total_state.total += 1
    if "ALLOCATED".lower() in node.node_state.lower() or "MIXED".lower() in node.node_state.lower():
        state.all_cluster_state[cluster_type].node_total_state.running += 1
    elif "IDLE".lower() in node.node_state.lower():
        state.all_cluster_state[cluster_type].node_total_state.available += 1
    else:
        state.all_cluster_state[cluster_type].node_total_state.unavailable += 1

    # 更新集群核心相关状态
    unavailable = node.all_core - node.free_core - node.used_core
    state.all_cluster_state[cluster_type].core_total_state.total += node.all_core
    state.all_cluster_state[cluster_type].core_total_state.running += node.used_core
    state.all_cluster_state[cluster_type].core_total_state.available += node.free_core
    state.all_cluster_state[cluster_type].core_total_state.unavailable += unavailable


def _get_node_type(node_name):
    if "gpu".lower() in node_name.lower():
        return "gpu"
    elif "compute".lower() in node_name.lower():
        return "cpu"
    else:
        return "other"
