import csv
import os

class DataLogger:
    def __init__(self, filename="game_data.csv"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["time", "ball_speed", "score_diff", "kicks", "jumps"])

    def log(self, time, ball_speed, score_diff, kicks, jumps):
        with open(self.filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([time, ball_speed, score_diff, kicks, jumps])