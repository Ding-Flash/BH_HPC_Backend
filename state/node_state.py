class NodeState:
    def __init__(self, node_name, node_state, all_core,
                 used_core, free_core, cpu_load,
                 memory, free_memory, node_type):
        self.node_name = node_name
        self.node_state = node_state
        self.all_core = all_core
        self.used_core = used_core
        self.free_core = free_core
        self.cpu_load = cpu_load
        self.memory = memory
        self.free_memory = free_memory
        self.node_type = node_type

    def __str__(self):
        return str(self.node_name) + ',' + \
               str(self.node_state) + ',' + \
               str(self.all_core) + ',' + \
               str(self.used_core) + ',' + \
               str(self.free_core) + ',' + \
               str(self.cpu_load) + ',' + \
               str(self.memory) + ',' + \
               str(self.free_memory) + ',' + \
               str(self.node_type)

    def to_dict(self):
        return {
            "node_name": self.node_name,
            "node_state": self.node_state,
            "all_core": self.all_core,
            "used_core": self.used_core,
            "free_core": self.free_core,
            "cpu_load": float(self.cpu_load),
            "memory": self.memory,
            "free_memory": self.free_memory,
            "node_type": self.node_type
        }
