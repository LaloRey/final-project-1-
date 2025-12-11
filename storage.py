"""This file handels saving the data to a csv file
if the file does not exists it creates it
"""
import csv
import os

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
