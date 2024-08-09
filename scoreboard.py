class ScoreBoard:

    def __init__(self, file_path):
        self.file_path = file_path
        self.scores = []

    def add_score(self, player_name, score):
        self.scores.append((player_name, score))

    def get_scores(self):
        return sorted(self.scores, key=lambda row: row[1], reverse=True)

    def __enter__(self):
        self.scores = []
        with open(self.file_path, 'a+') as in_file:
            in_file.seek(0)
            for line in in_file:
                player, score = line.split(',')
                score = int(score)
                self.scores.append((player, score))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.file_path, 'w') as out_file:
            for player, score in self.get_scores()[:100]:
                out_file.write(f'{player},{score}\n')
