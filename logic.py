from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtGui import QIntValidator


import csv
import os
from gui import Ui_Gradechecker
from storage import CsvStorage

"""
This file contains the logic for the application. Checks the math for the grade checker.
It makes sure the names are valid, the number of attempts is valid and the scores are valid.
It also calculates the final grade and gets the highest score.
"""
CSV_FILE =  "data/grades.csv"
"""This creates a file called grades.csv and makes it a variable."""

class GradeResult:
    """This class holds the result of the grade calculation"""

    def __init__(self, name, scores, final):
        self.name = name
        self.scores = scores
        self.final = final
class GradeCheckerWindow(QMainWindow, Ui_Gradechecker):
    """This class controls everything the user sees ands clicks"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.manager = GradeManager()
        self.storage = CsvStorage(CSV_FILE)

        self.numLine.setValidator(QIntValidator(1, 4, self))

        self.scoreLine.setValidator(QIntValidator(0, 100, self))
        self.scoreLine_2.setValidator(QIntValidator(0, 100, self))
        self.scoreLine_3.setValidator(QIntValidator(0, 100, self))
        self.scoreLine_4.setValidator(QIntValidator(0, 100, self))

        self.numLine.textChanged.connect(self.update_score_boxes)

        self.gradeBtn.clicked.connect(self.submit_form)

        self.update_score_boxes()
        self.show_message("", kind="info")
        self.setWindowTitle("Grade Checker")
#--------------------------------UI Helpers------------------------------------
    def update_score_boxes(self):
        """This method updates the visibility of the score boxes depending on the number of attempts"""

        text = self.numLine.text().strip()
        try:
            attempts = int(text)
        except:
             attempts = 1

        if attempts < 1:
            attempts = 1
        if attempts > 4:
            attempts = 4
        """if you click one it only shows one line but if you click more then one it shows the line 
        up to 4 lines total and wont go futher.
        """
        self.scoreLabel.setVisible(attempts >= 1)
        self.scoreLine.setVisible(attempts >= 1)

        self.scoreLabel_2.setVisible(attempts >= 2)
        self.scoreLine_2.setVisible(attempts >= 2)

        self.scoreLabel_3.setVisible(attempts >= 3)
        self.scoreLine_3.setVisible(attempts >= 3)

        self.scoreLabel_4.setVisible(attempts >= 4)
        self.scoreLine_4.setVisible(attempts >= 4)

    def show_message(self, text, kind="info"):
        """This method shows a message in the status bar like errors or successes"""

        if kind == "info":
            color = "red"
        elif kind == "success":
            color = "green"
        else:
            color = "black"
        """after eaither showing succses or error it will change to red for error or 
        green for success.
        """
        self.statuslabel.setStyleSheet(f"color: {color}; font-weight: bold;")
        self.statuslabel.setText(text)
    #---------------------------------------------------------------------------------

    def submit_form(self):
        """Checks all the users inputs, finds the highest score, saves the results  """
        try:
            name_input = self.studentLine.text()
            attempts_input = self.numLine.text()


            attempts = self.manager.validate_attempts(attempts_input)


            score_inputs = []
            if attempts >= 1:
                score_inputs.append(self.scoreLine.text())
            if attempts >= 2:
                score_inputs.append(self.scoreLine_2.text())
            if attempts >= 3:
                score_inputs.append(self.scoreLine_3.text())
            if attempts >= 4:
                score_inputs.append(self.scoreLine_4.text())


            result = self.manager.build_result(name_input, attempts_input, score_inputs)


            self.storage.append(result.name, result.scores, result.final)

        except ValueError as problem:
            self.show_message(str(problem), kind="error")
            return

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error: {e}")
            self.show_message(f"Unexpected error: {e}", kind="error")
            return

        else:
            self.show_message("Submitted!", kind="success")

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
            raise ValueError("Attempts must be between 1 and 4")
        if attempts < 1 or attempts > 4:
            raise ValueError("Attempts must be between 1 and 4")
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

"""This class handels saving the data to a csv file
if the file does not exists it creates it
"""


class CsvStorage:
    """This class saves the data to a csv file"""

    def __init__(self, filename: str) -> None:
        """Creates the file if it does not exist"""
        self.filename = filename

        folder = os.path.dirname(filename)
        if folder != "" and not os.path.exists(folder):
            os.makedirs(folder)

        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Score 1", "Score 2", "Score 3", "Score 4", "Final"])

    def append(self, name: str, scores4: list[int], final: int) -> None:
        """Appends the data to the file, adds studnets name, scores and final score to the CSV file """

        with open(self.filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([name, scores4[0], scores4[1], scores4[2], scores4[3], final])



