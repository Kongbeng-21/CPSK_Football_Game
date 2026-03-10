class Goal:
    def __init__(self,x,width):
        self.x = x
        self.width = width

    def check_goal(self,ball):
        if ball.x < self.x + self.width:
            return True
        return False