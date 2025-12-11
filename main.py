import sys
from controller import GradeCheckerWindow
from PyQt6.QtWidgets import QApplication


def main():
    """This is the main function that runs the application and opens the gui"""
    app = QApplication(sys.argv)
    window = GradeCheckerWindow()
    window.show()
    sys.exit(app.exec())




if __name__ == "__main__":
    main()
