import pickle
class specific_logger():
    def __init__(self, entity_name):
        self.step_lst = []
        self.step_count = 0
        self.entity_name = entity_name

    def add_new_log(self, new_step):
        self.step_count += 1
        self.step_lst.append(f"Step {self.step_count}: {new_step}")

    def generate(self, filename):
        with open(f"{self.entity_name}_log.bin", "wb") as binary_file:
            pickle.dump(self.step_lst, binary_file)
    def __str__(self):
        result = "\n".join(self.step_lst)
        return result


