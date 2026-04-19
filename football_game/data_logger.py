import csv
import os

class DataLogger:
    def __init__(self, filename="game_data.csv"):
        self.filename = filename
        self.headers = [
            "time",
            "ball_speed",
            "score_p1",
            "score_p2",
            "score_diff",
            "kicks_p1",
            "kicks_p2",
            "jumps_p1",
            "jumps_p2",
            "possession",
            "ball_zone",
            "attacking_side",
            "touches_p1",
            "touches_p2",
            "shots_p1",
            "shots_p2",
            "winner",
        ]

        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)

    def log(self, row):
        with open(self.filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)
