"""
This file contains the logic for the application. Checks the math for the grade checker.
It makes sure the names are valid, the number of attempts is valid and the scores are valid.
It also calculates the final grade and gets the highest score.
"""
class GradeResult:
    """This class holds the result of the grade calculation"""

    def __init__(self, name, scores, final):
        self.name = name
        self.scores = scores
        self.final = final

class GradeManager:
    """This class contains the logic for the grade checker
"""

    def validate_name(self, user_input: str) -> str:
        """Checks that the name is not empty"""
        if user_input is None:
            raise ValueError("Name cannot be empty")
        name = user_input.strip()
        if name == "":
            raise ValueError("Name cannot be empty")
        return name

    def validate_attempts(self, user_input: str)-> int:
        """Checks that the number of attempts is between 1 and 4"""
        try:
            attempts = int(user_input.strip())
        except:
            raise ValueError("Attempts must be a number between 1 and 4")
        if attempts < 1 or attempts > 4:
            raise ValueError("Attempts must be a number between 1 and 4")
        return attempts

    def validate_scores(self, score_inputs: list[str], attempts: int) -> list[int]:
        """Checks that the scores are valid integers between 0 and 100"""

        scores = []
        for i in range(attempts):
            text = score_inputs[i].strip()

            try :
                score = int(text)
            except ValueError:
                raise ValueError(f" Score {i+1} must be a number between 0 and 100")
            if score < 0 or score > 100:
                raise ValueError(f" Score {i+1} must be a number between 0 and 100")

            scores.append(score)

        while len(scores) < 4:
            scores.append(0)

        return scores

    def final_grade(self, scores_list: list[int]) -> int:
        """Calculates the final grade based on the scores ands which one is the highest"""

        return max(scores_list)

    def build_result(self, name_input, attempts_input, score_inputs):
        """Builds the result object from the inputs and puts the in varables used by main"""
        name = self.validate_name(name_input)
        attempts = self.validate_attempts(attempts_input)
        scores4 = self.validate_scores(score_inputs, attempts)
        final = self.final_grade(scores4)
        return GradeResult(name, scores4, final)



