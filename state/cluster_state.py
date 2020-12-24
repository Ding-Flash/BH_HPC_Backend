import state
from state.base_class import EntiretyState


##########################################
# CPU集群状态
##########################################
class CPUClusterState(EntiretyState):
    def __init__(self):
        super().__init__()

    def to_dict(self):
        return {
            "cpu": super(CPUClusterState, self).to_dict()
        }


##########################################
# GPU集群状态
##########################################
class GPUClusterState(EntiretyState):
    def __init__(self):
        super().__init__()

    def to_dict(self):
        return {
            "gpu": super(GPUClusterState, self).to_dict()
        }


##########################################
# GPU集群状态
##########################################
class OtherClusterState(EntiretyState):
    def __init__(self):
        super().__init__()

    def to_dict(self):
        return {
            "other": super(OtherClusterState, self).to_dict()
        }


##########################################
# 总体集群状态
##########################################
class EntireClusterState(EntiretyState):
    def __init__(self):
        super().__init__()

    def update_state(self):
        for cluster_state in state.all_cluster_state.values():
            self.node_total_state.total += cluster_state.node_total_state.total
            self.node_total_state.running += cluster_state.node_total_state.running
            self.node_total_state.available += cluster_state.node_total_state.available
            self.node_total_state.unavailable += cluster_state.node_total_state.unavailable

            self.core_total_state.total += cluster_state.core_total_state.total
            self.core_total_state.running += cluster_state.core_total_state.running
            self.core_total_state.available += cluster_state.core_total_state.available
            self.core_total_state.unavailable += cluster_state.core_total_state.unavailable

    def to_dict(self):
        return {
            "cluster": super(EntireClusterState, self).to_dict()
        }

    def clear(self):
        super(EntireClusterState, self).clear()
        for cluster_state in state.all_cluster_state.values():
            cluster_state.clear()
