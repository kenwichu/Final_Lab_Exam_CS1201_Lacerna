class Score:
    def __init__(self, username, points, stages_won, date):
        self.username = username
        self.points = points
        self.stages_won = stages_won
        self.date = date

    def __repr__(self):
        return f"Username: {self.username}, Points: {self.points}, Wins: {self.stages_won}, Date: {self.date}"
