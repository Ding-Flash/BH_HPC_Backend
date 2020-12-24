############################################################################
# 节点及核心状态基类
############################################################################


class State:
    def __init__(self, total=0, running=0, available=0, unavailable=0):
        self.total = total
        self.running = running
        self.available = available
        self.unavailable = unavailable

    def to_dict(self):
        return {
            "total": self.total,
            "running": self.running,
            "available": self.available,
            "unavailable": self.unavailable
        }

    def clear(self):
        self.total = 0
        self.running = 0
        self.available = 0
        self.unavailable = 0


# 节点状态
class NodeTotalState(State):
    def __init__(self, total=0, running=0, available=0, unavailable=0):
        super().__init__(total, running, available, unavailable)

    def to_dict(self):
        return {
            "node": super(NodeTotalState, self).to_dict()
        }


# 核心状态
class CoreTotalState(State):
    def __init__(self, total=0, running=0, available=0, unavailable=0):
        super().__init__(total, running, available, unavailable)

    def to_dict(self):
        return {
            "core": super(CoreTotalState, self).to_dict()
        }


class EntiretyState:
    def __init__(self):
        self.node_total_state = NodeTotalState()
        self.core_total_state = CoreTotalState()

    def to_dict(self):
        return {
            **self.node_total_state.to_dict(),
            **self.core_total_state.to_dict()
        }

    def clear(self):
        self.node_total_state.clear()
        self.core_total_state.clear()


# 任务队列状态基类
class QueueStateBase:
    def __init__(self):
        self.job_total = 0
        self.job_running = 0
        self.job_waiting = 0
        self.user_total = set()
        self.user_running = set()
        self.user_waiting = set()

    def clear(self):
        self.job_total = 0
        self.job_running = 0
        self.job_waiting = 0
        self.user_total = set()
        self.user_running = set()
        self.user_waiting = set()

    def get_user_total_num(self):
        return len(self.user_total)

    def get_user_running_num(self):
        return len(self.user_running)

    def get_user_waiting_num(self):
        return len(self.user_waiting)

    def to_dict(self):
        return {
            'job': {
                'total': self.job_total,
                'running': self.job_running,
                'waiting': self.job_waiting
            },
            'user': {
                'total': self.get_user_total_num(),
                'running': self.get_user_running_num(),
                'waiting': self.get_user_waiting_num()
            }
        }
