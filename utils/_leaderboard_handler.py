"""Leaderboard Score Handler"""
import json


class ScoreHandler():
    """Class to handle the stored player scores."""
    def __init__(self):
        self.load_scores()

    def load_scores(self):
        """Load the leaderboard from external json file and convert to Python
        data structures."""
        with open("scores.json", "r") as file:
            contents = file.read()

        self.scores = json.loads(contents)

    def get_top_10(self):
        """Return the top 10 scores in a list. If there are less than 10 score
        entries, it is padded with blank tuples."""
        top = []

        counter = 0
        for item, counter in zip(self.scores.items(), range(10)):
            top.append(item)

        # if less than 10 scores added to list
        if counter != 9:
            # find number of empty score entries to add
            entries_added = counter + 1
            entries_empty = 10 - entries_added

            # add empty score entries
            # _ used as counter variable as it doesn't get used
            # the value isn't important
            for _ in range(entries_empty):
                top.append(("---", "--"))

        return top

    def save_scores(self):
        """Sort the scores in the scores attribute and then overwrite the
        scores.json file with the sorted scores."""
        sorted_scores = {}

        # iterate through the scores attribute in order of descending order of
        # the value for each key:value pair
        # reverse argument makes it descending
        # key argument specifies to order based on the key efficiently with
        # lambda function
        for key, value in sorted(self.scores.items(), reverse=True,
                                 key=lambda x: x[1]):
            sorted_scores[key] = value

        # overwrite file with new scores in json format
        with open("scores.json", "w") as file:
            file.write(json.dumps(sorted_scores) + "\n")

    def add_score(self, username, new_score):
        """Add a score to the scores attribute. If a player scored lower than
        previous attempt, don't update score.
        Returns if score was updated or not."""
        # if they have existing score
        if username in self.scores:
            if self.scores[username] >= new_score:
                return False

        self.scores[username] = new_score  # add/update key with new value
        self.save_scores()  # sort scores and save to file
        self.load_scores()  # reload scores to use sorted dict with new score
        return True
