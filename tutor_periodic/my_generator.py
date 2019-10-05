from tutorsim.system_simulator import SystemSimulator
from tutorsim.behavior_model_executor import BehaviorModelExecutor
from tutorsim.system_message import SysMessage
from tutorsim.definition import *

class Generator(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        # Open CSV
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("ASSESS", 1)
        self.insert_state("WAIT", 300)

        self.insert_input_port("start")
        self.insert_output_port("process")

        self.student_list = []

    def ext_trans(self,port, msg):
        if port == "start":
            #print("start")
            self._cur_state = "ASSESS"
            data = msg.retrieve()
            self.process_studnets_list(data[0])

    def output(self):
        #temp = "[%f]" % (SystemSimulator().get_engine(self.engine_name).get_global_time())
        student = self.student_list.pop(0)
        msg = SysMessage(self.get_name(), "process")
        #print(str(datetime.datetime.now()) + " Human Object:")
        msg.insert(student)
        return msg
        
    def int_trans(self):
        if self._cur_state == "ASSESS" and not self.student_list:
            self._cur_state = "WAIT"
        else:
            self._cur_state = "ASSESS"

    def process_studnets_list(self, student_list):
        f = open(student_list, "r")
        for line in f:
            self.student_list.append(line.strip())
        pass