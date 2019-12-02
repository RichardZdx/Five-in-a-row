class Chess():
    def __init__(self):
        self.hori = 1
        self.vert = 1
        self.lt = 1
        self.rt = 1
        self.sign = 0
        self.top_ex = 0
        self.bot_ex = 0
        self.left_ex = 0
        self.right_ex = 0
        self.lt_ex = 0
        self.rb_ex = 0
        self.rt_ex = 0
        self.lb_ex = 0

    def set_to_black(self):
        self.sign = -1

    def set_to_white(self):
        self.sign = 1

    def get_max(self):
        return max(self.hori, self.vert, self.lt, self.rt)
