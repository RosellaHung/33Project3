class steplogger:
    def __init__(self):
        self.step_lst = []
        self.step_count = 0

    def add_new_log(self, new_step):
        self.step_count += 1
        self.step_lst.append(f"step {self.step_count}: {new_step}")

    def __str__(self):
        for step in self.step_lst:
            print(step)