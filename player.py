import csv
from datetime import date


class Player:
    def __init__(self):
        self.score = 0
        self.timer = 0
        self.name = ""
        self.speed = 1
        self.mode = 1
        self.start_speed = 1

    def format_timer(self):
        mins = self.timer // 60
        formatted_mins = f"0{mins}" if mins < 10 else mins
        secs = self.timer - mins * 60
        formatted_secs = f"0{secs}" if secs < 10 else secs
        formatted_timer = f"{formatted_mins}:{formatted_secs}"

        return formatted_timer

    def save_score(self, format_timer):
        with open("scores.csv", "a+") as f:
            f.seek(0)
            data = f.read(100)
            if len(data) > 0:
                f.write("\n")
            f.write(
                f"{self.name},{str(self.score)},{round(self.speed, 1)},{format_timer()},{date.today()}"
            )

    @staticmethod
    def get_max_score():
        rows = []
        with open("scores.csv", "a+") as f:
            f.seek(0)
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                rows.append(int(row[1]))
        if len(rows) > 0:
            max_score = sorted(rows, reverse=True)
            return max_score[0]

    def restart_stats(self):
        self.score = 0
        self.timer = 0
        self.name = ""
        self.speed = self.start_speed
