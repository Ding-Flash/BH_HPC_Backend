import datetime


class JobState:
    def __init__(self, job_name, account, user,
                 partition, qos, num_node,
                 num_core, state, time, des):
        self.job_name = job_name
        self.account = account
        self.user = user
        self.partition = partition
        self.qos = qos
        self.num_node = num_node
        self.num_core = num_core
        self.state = state
        self.time = time
        self.des = des

    def __str__(self):
        return str(self.job_name) + ',' + \
               str(self.account) + ',' + \
               str(self.user) + ',' + \
               str(self.partition) + ',' + \
               str(self.qos) + ',' + \
               str(self.num_node) + ',' + \
               str(self.num_core) + ',' + \
               str(self.state) + ',' + \
               str(self.time) + ',' + \
               str(self.des)

    def to_dict(self):
        return {
            "job_name": self.job_name,
            "account": self.account,
            "user": self.user,
            "partition": self.partition,
            "qos": self.qos,
            "num_node": self.num_node,
            "num_core": self.num_core,
            "state": self.state,
            "time_string": self.get_time_delta_sec(),
            "time": self.time.total_seconds(),
            "des": self.des,
        }

    def get_time_delta_sec(self):
        m, s = divmod(int(self.time.total_seconds()), 60)
        h, m = divmod(m, 60)
        return "{:0>2d}:{:0>2d}:{:0>2d}".format(h, m, s)
