import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QSpinBox, QComboBox, QFormLayout
)
from PyQt5.QtCore import Qt


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #f0f4ff;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("🏠 Home Page")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignCenter)

        self.info_label = QLabel("Welcome! Please fill in your profile.")
        self.info_label.setStyleSheet("font-size: 14px; color: #555;")
        self.info_label.setAlignment(Qt.AlignCenter)

        name_label = QLabel("Name:")
        name_label.setStyleSheet("font-size: 14px;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.name_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #aaa; border-radius: 6px;")
        self.name_input.setFixedWidth(280)

        email_label = QLabel("Email:")
        email_label.setStyleSheet("font-size: 14px;")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #aaa; border-radius: 6px;")
        self.email_input.setFixedWidth(280)

        # Display area for returned data (optional)
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-size: 13px; color: #2a7ae2; background: #e8f0fe; padding: 10px; border-radius: 8px;")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)
        self.result_label.setFixedWidth(300)
        self.result_label.hide()

        next_btn = QPushButton("Next ➡")
        next_btn.setFixedWidth(160)
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90d9; color: white;
                padding: 10px; font-size: 15px;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #357abd; }
        """)
        next_btn.clicked.connect(self.go_next)

        layout.addWidget(title)
        layout.addWidget(self.info_label)
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.result_label)
        layout.addWidget(next_btn)
        self.setLayout(layout)

    def go_next(self):
        self.window().stack.setCurrentIndex(1)

    def show_result(self, name, email, age, major):
        self.result_label.setText(
            f"👤 Name: {name}\n📧 Email: {email}\n🎂 Age: {age}\n🎓 Major: {major}"
        )
        self.result_label.show()


class ProfilePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fff8f0;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("👤 Profile Page")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Your name & email info goes here.")
        subtitle.setStyleSheet("font-size: 13px; color: #777;")
        subtitle.setAlignment(Qt.AlignCenter)

        self.display_label = QLabel("")
        self.display_label.setStyleSheet("font-size: 14px; color: #444; background: #fff3e0; padding: 10px; border-radius: 8px;")
        self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setFixedWidth(300)

        next_btn = QPushButton("Next ➡ (Age & Major)")
        next_btn.setFixedWidth(220)
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: #e67e22; color: white;
                padding: 10px; font-size: 15px; border-radius: 8px;
            }
            QPushButton:hover { background-color: #ca6f1e; }
        """)
        next_btn.clicked.connect(self.go_next)

        back_btn = QPushButton("⬅ Back")
        back_btn.setFixedWidth(120)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #aaa; color: white;
                padding: 8px; font-size: 14px; border-radius: 8px;
            }
            QPushButton:hover { background-color: #888; }
        """)
        back_btn.clicked.connect(self.go_back)

        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignCenter)
        btn_row.addWidget(back_btn)
        btn_row.addWidget(next_btn)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.display_label)
        layout.addLayout(btn_row)
        self.setLayout(layout)

    def go_next(self):
        home = self.window().stack.widget(0)
        name = home.name_input.text()
        email = home.email_input.text()
        self.display_label.setText(f"Name: {name}\nEmail: {email}")
        self.window().stack.setCurrentIndex(2)

    def go_back(self):
        self.window().stack.setCurrentIndex(0)


class AgeMajorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #f0fff4;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("📋 Age & Major Page")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignCenter)

        form = QFormLayout()
        form.setSpacing(12)

        self.age_spin = QSpinBox()
        self.age_spin.setRange(1, 120)
        self.age_spin.setValue(18)
        self.age_spin.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #aaa; border-radius: 6px;")
        self.age_spin.setFixedWidth(120)

        self.major_combo = QComboBox()
        self.major_combo.addItems(["DME", "CoE"])
        self.major_combo.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #aaa; border-radius: 6px;")
        self.major_combo.setFixedWidth(180)

        age_label = QLabel("Age:")
        age_label.setStyleSheet("font-size: 14px;")
        major_label = QLabel("Major:")
        major_label.setStyleSheet("font-size: 14px;")

        form.addRow(age_label, self.age_spin)
        form.addRow(major_label, self.major_combo)

        done_btn = QPushButton("✅ Done")
        done_btn.setFixedWidth(160)
        done_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                padding: 10px; font-size: 15px; border-radius: 8px;
            }
            QPushButton:hover { background-color: #1e8449; }
        """)
        done_btn.clicked.connect(self.go_done)

        back_btn = QPushButton("⬅ Back")
        back_btn.setFixedWidth(120)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #aaa; color: white;
                padding: 8px; font-size: 14px; border-radius: 8px;
            }
            QPushButton:hover { background-color: #888; }
        """)
        back_btn.clicked.connect(self.go_back)

        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignCenter)
        btn_row.addWidget(back_btn)
        btn_row.addWidget(done_btn)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addLayout(btn_row)
        self.setLayout(layout)

    def go_done(self):
        home = self.window().stack.widget(0)
        name = home.name_input.text()
        email = home.email_input.text()
        age = self.age_spin.value()
        major = self.major_combo.currentText()
        home.show_result(name, email, age, major)
        self.window().stack.setCurrentIndex(0)

    def go_back(self):
        self.window().stack.setCurrentIndex(1)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3-Page Stack App")
        self.setFixedSize(500, 450)

        self.stack = QStackedWidget()
        self.stack.addWidget(HomePage())     # index 0
        self.stack.addWidget(ProfilePage())  # index 1
        self.stack.addWidget(AgeMajorPage()) # index 2

        self.setCentralWidget(self.stack)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())