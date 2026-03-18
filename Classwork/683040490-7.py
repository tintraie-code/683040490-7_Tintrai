import sys
import csv
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QFileDialog, QLineEdit, QMessageBox
)


class StudentManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Score Manager")
        self.resize(700, 500)

        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        btn_layout = QHBoxLayout()
        self.btn_load = QPushButton("Load CSV")
        self.btn_save = QPushButton("Save CSV")
        self.lbl_file = QLabel("No file loaded")
        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.lbl_file)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Score", "Grade"])

        add_layout = QHBoxLayout()
        self.input_name  = QLineEdit(); self.input_name.setPlaceholderText("Name")
        self.input_score = QLineEdit(); self.input_score.setPlaceholderText("Score")
        self.input_grade = QLineEdit(); self.input_grade.setPlaceholderText("Grade")
        self.btn_add = QPushButton("Add Row")
        add_layout.addWidget(self.input_name)
        add_layout.addWidget(self.input_score)
        add_layout.addWidget(self.input_grade)
        add_layout.addWidget(self.btn_add)

        layout.addLayout(btn_layout)
        layout.addWidget(self.table)
        layout.addLayout(add_layout)

        self.btn_load.clicked.connect(self.load_file)
        self.btn_save.clicked.connect(self.save_file)
        self.btn_add.clicked.connect(self.add_row)

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        self.lbl_file.setText(path.split("/")[-1])
        self.table.setRowCount(0)

        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                r = self.table.rowCount()
                self.table.insertRow(r)
                self.table.setItem(r, 0, QTableWidgetItem(row["name"]))
                self.table.setItem(r, 1, QTableWidgetItem(row["score"]))
                self.table.setItem(r, 2, QTableWidgetItem(row["grade"]))

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "score", "grade"])
            for r in range(self.table.rowCount()):
                writer.writerow([
                    self.table.item(r, 0).text(),
                    self.table.item(r, 1).text(),
                    self.table.item(r, 2).text(),
                ])

    def add_row(self):
        name  = self.input_name.text().strip()
        score = self.input_score.text().strip()
        grade = self.input_grade.text().strip()

        if not name or not score or not grade:
            QMessageBox.warning(self, "Missing Data", "Please fill in all fields")
            return

        r = self.table.rowCount()
        self.table.insertRow(r)
        self.table.setItem(r, 0, QTableWidgetItem(name))
        self.table.setItem(r, 1, QTableWidgetItem(score))
        self.table.setItem(r, 2, QTableWidgetItem(grade))

        self.input_name.clear()
        self.input_score.clear()
        self.input_grade.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = StudentManager()
    win.show()
    sys.exit(app.exec())