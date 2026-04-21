import csv
import os

class DataLogger:
    def __init__(self, filename="game_data.csv"):
        self.filename = filename
        self.headers = [
            "match_id",
            "time",
            "match_duration",
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
                
    def get_next_match_id(self):
        max_match_id = 0

        if not os.path.exists(self.filename):
            return 1

        with open(self.filename, "r", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    max_match_id = max(max_match_id, int(row["match_id"]))
                except (KeyError, TypeError, ValueError):
                    pass

        return max_match_id + 1

    def log(self, row):
        with open(self.filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)
