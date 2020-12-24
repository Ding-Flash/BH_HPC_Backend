import state
from state.base_class import QueueStateBase


##########################################
# CPU任务状态
##########################################
class CPUQueueState(QueueStateBase):
    def __init__(self):
        super(CPUQueueState, self).__init__()

    def to_dict(self):
        return {
            'cpu': super(CPUQueueState, self).to_dict()
        }


##########################################
# GPU任务状态
##########################################
class GPUQueueState(QueueStateBase):
    def __init__(self):
        super(GPUQueueState, self).__init__()

    def to_dict(self):
        return {
            'gpu': super(GPUQueueState, self).to_dict()
        }


##########################################
# 其他任务状态
##########################################
class OtherQueueState(QueueStateBase):
    def __init__(self):
        super(OtherQueueState, self).__init__()

    def to_dict(self):
        return {
            'other': super(OtherQueueState, self).to_dict()
        }


##########################################
# 全部任务状态
##########################################
class EntireQueueState(QueueStateBase):
    def __init__(self):
        super(EntireQueueState, self).__init__()

    def to_dict(self):
        return {
            'entire': super(EntireQueueState, self).to_dict()
        }

    def update_state(self):
        for queue_state in state.all_queue_state.values():
            self.job_total += queue_state.job_total
            self.job_running += queue_state.job_running
            self.job_waiting += queue_state.job_waiting
            self.user_total.update(queue_state.user_total)
            self.user_waiting.update(queue_state.user_waiting)
            self.user_running.update(queue_state.user_running)

    def clear(self):
        super(EntireQueueState, self).clear()
        for queue_state in state.all_queue_state.values():
            queue_state.clear()
