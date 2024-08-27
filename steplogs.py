import pickle
class steplogger:
    def __init__(self):
        self.step_lst = []
        self.step_count = 0

    def add_new_log(self, new_step):
        self.step_count += 1
        self.step_lst.append(f"Step {self.step_count}: {new_step}")

    def __str__(self):
        return "\n".join(self.step_lst)


class specific_logger(steplogger):
    def __init__(self, entity_name):
        super().__init__()
        self.entity_name = entity_name

    def write_new(self, event):
        self.add_new_log(event)

    def __call__(self, filename):
        with open(f"{self.entity_name}_log.pkl", "wb") as binary_file:
            pickle.dump(self.step_lst, binary_file)
