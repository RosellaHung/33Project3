import pickle
class steplogger:
    def __init__(self):
        self.step_lst = []
        self.step_count = 0

    def add_new_log(self, new_step):
        self.step_count += 1
        self.step_lst.append(f"Step {self.step_count}: {new_step}")

    def __str__(self):
        for step in self.step_lst:
            print(step)

class specific_logger(steplogger):
    def __init__(self, entity_name):
        super().__init__()
        self.entity_name = entity_name

    # def add_new_log(self, new_event):
    #     self.step_count += 1
    #     self.step_lst.append(f"Step {self.step_count}: {new_event}")

    def generate(self, filename):
        with open(f"{self.entity_name}_log.bin", "wb") as binary_file:
            pickle.dump(self.step_lst, binary_file)

#do we only generate binary file when device is called?



