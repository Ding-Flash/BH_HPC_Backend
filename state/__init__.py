import collections

from state.base_class import CoreTotalState, NodeTotalState
from state.cluster_state import CPUClusterState, GPUClusterState, EntireClusterState, OtherClusterState

# 初始化状态
from state.queue_state import CPUQueueState, GPUQueueState, OtherQueueState, EntireQueueState

all_cluster_state = collections.OrderedDict({
    # 初始化CPU集群状态
    "cpu_cluster_state": CPUClusterState(),
    # 初始化GPU集群状态
    "gpu_cluster_state": GPUClusterState(),
    # 初始化其他类型节点的状态
    "other_cluster_state": OtherClusterState()
})
# 初始化集群总体状态实例,需要在根据数据库更新CPU及GPU集群后重新执行update_cluster_state方法更新状态
entire_cluster_state = EntireClusterState()

all_queue_state = collections.OrderedDict({
    # 初始化CPU任务状态
    "cpu_queue_state": CPUQueueState(),
    # 初始化GPU任务状态
    "gpu_queue_state": GPUQueueState(),
    # 初始化其他任务状态
    "other_queue_state": OtherQueueState()
})

entire_queue_state = EntireQueueState()

job_state_list = []
node_state_list = []
