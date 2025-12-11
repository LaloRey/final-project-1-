from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtGui import QIntValidator
import sys



from grades import Ui_Gradechecker
from logic import GradeManager
from storage import CsvStorage

CSV_FILE =  "data/grades.csv"
"""
This is the main file for the grade checker application.
it contains the window on the screen and lets the user type there name,
number of attempts and scores for each attempt. When the user clicks submit,
the data is validated and stored in a csv file.
"""
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

        self.statuslabel.setStyleSheet(f"color: {color}; font-weight: bold;")
        self.statuslabel.setText(text)
    #---------------------------------------------------------------------------------

    def submit_form(self):
        """Checks all the users inputs, finds the highest score, saves the resultys  """
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


def main():
    """This is the main function that runs the application and opens the gui"""
    app = QApplication(sys.argv)
    window = GradeCheckerWindow()
    window.show()
    sys.exit(app.exec())




if __name__ == "__main__":
    main()
