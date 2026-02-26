from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
    QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton,
    QFrame, QSpinBox, QColorDialog, QFileDialog, QToolBar, QStyle
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QAction, QPixmap
import sys, os, pyperclip

dir = os.path.dirname(os.path.abspath(__file__))
default_color = "#FF96C5"


class PersonalCard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: Personal Info Card")
        self.setGeometry(100, 100, 400, 460)

        # Rainbow animation state
        self.rainbow_hue = 0
        self.rainbow_timer = QTimer()
        self.rainbow_timer.timeout.connect(self._animate_rainbow)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.addSpacing(15)

        self.create_form()

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #cccccc;")
        self.main_layout.addWidget(line)
        self.main_layout.addSpacing(15)

        self.bg_widget = QWidget()
        self.output_layout = QVBoxLayout(self.bg_widget)
        self.create_display()
        self.main_layout.addWidget(self.bg_widget)

        self.create_menu()
        self.create_toolbar()

        self.statusBar().showMessage("Fill in your details and click generate")

    def create_form(self):
        form_layout = QFormLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Your name")
        self.age = QSpinBox()
        self.age.setRange(1, 120)
        self.age.setValue(25)

        self.email = QLineEdit()
        self.email.setPlaceholderText("example@gmail.com")
        self.position = QComboBox()
        self.position.addItems(["Teaching Staff", "Supporting Staff", "Student", "Visitor"])
        self.position.setCurrentIndex(-1)

        self.fav_color = QColor(default_color)
        self.color_swatch = QLabel()
        self.color_swatch.setFixedSize(22, 22)
        self.color_swatch.setStyleSheet(f"background-color:{self.fav_color.name()};border:1px solid #888;")

        color_btn = QPushButton("Pick Color")
        color_btn.clicked.connect(self.pick_color)

        color_row = QHBoxLayout()
        color_row.addWidget(self.color_swatch)
        color_row.addWidget(color_btn)

        form_layout.addRow("Full name:", self.name)
        form_layout.addRow("Age:", self.age)
        form_layout.addRow("Email:", self.email)
        form_layout.addRow("Position:", self.position)
        form_layout.addRow("Favorite color:", QWidget())
        form_layout.itemAt(form_layout.rowCount()-1, QFormLayout.FieldRole).widget().setLayout(color_row)

        self.main_layout.addLayout(form_layout)

    def pick_color(self):
        # Stop rainbow if active when picking a solid color
        self.rainbow_timer.stop()
        color = QColorDialog.getColor(self.fav_color, self)
        if color.isValid():
            self.fav_color = color
            self.color_swatch.setStyleSheet(f"background-color:{color.name()};border:1px solid #888;")

    def create_display(self):
        self.bg_widget.setStyleSheet(f"background-color:{default_color};border-radius:6px;")

        self.name_label = QLabel("Your name")
        self.name_label.setStyleSheet("font-size:18pt;font-weight:bold;")
        self.age_label = QLabel("(Age)")
        self.position_label = QLabel("Position")
        self.position_label.setStyleSheet("font-size:14pt;")
        email_icon = QLabel()
        email__icon_file = os.path.join(dir, "Tinmail.png")
        email_icon.setPixmap(QPixmap(email__icon_file).scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.email_label = QLabel("example@gmail.com")
        email_layout = QHBoxLayout()
        email_layout.addWidget(email_icon)
        email_layout.addWidget(self.email_label)
        email_layout.addStretch()
        self.output_layout.addWidget(self.name_label)
        self.output_layout.addWidget(self.age_label)
        self.output_layout.addStretch()
        self.output_layout.addWidget(self.position_label)
        self.output_layout.addLayout(email_layout)
        self.output_layout.addSpacing(10)
        self.main_layout.addWidget(self.bg_widget)

    def update_display(self):
        if "@" not in self.email.text() or self.position.currentIndex() == -1 or not self.name.text().strip():
            self.statusBar().showMessage("Please fill in all fields with vaild data", 3000)
            return
        self.name_label.setText(self.name.text() or "Your name")
        self.age_label.setText(f"({self.age.value()})")
        self.position_label.setText(self.position.currentText() or "Position")
        self.email_label.setText(self.email.text() or "example@gmail.com")
        # Stop rainbow and use selected color
        self.rainbow_timer.stop()
        self.bg_widget.setStyleSheet(f"background-color:{self.fav_color.name()};border-radius:6px;")
        self.statusBar().showMessage("Card generated and displaying", 3000)

    def set_rainbow_bg(self):
        """Start rainbow animation on the card background."""
        self.rainbow_timer.start(1)  # Update every 50ms
        self.statusBar().showMessage("🌈 Rainbow mode activated!", 3000)

    def _animate_rainbow(self):
        """Called by timer to cycle through hues."""
        self.rainbow_hue = (self.rainbow_hue + 3) % 360
        color = QColor.fromHsv(self.rainbow_hue, 200, 255)
        self.bg_widget.setStyleSheet(
            f"background-color:{color.name()}; border-radius:6px;"
        )

    def clear_form(self):
        self.name.clear()
        self.age.setValue(25)
        self.email.clear()
        self.position.setCurrentIndex(-1)
        self.statusBar().showMessage("Form cleared", 3000)

    def clear_display(self):
        self.rainbow_timer.stop()
        self.name_label.setText("Your name")
        self.age_label.setText("(Age)")
        self.position_label.setText("Position")
        self.email_label.setText("email@domain")
        self.bg_widget.setStyleSheet(f"background-color:{default_color};border-radius:6px;")
        self.statusBar().showMessage("Display cleared", 3000)

    def clear_all(self):
        self.clear_form()
        self.clear_display()
        self.statusBar().showMessage("Form & Display cleared", 3000)

    def save_card(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Card", "my_card.txt", "Text Files (*.txt)")
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(
                    f"{self.name_label.text()}\n"
                    f"{self.age_label.text()}\n"
                    f"{self.position_label.text()}\n"
                    f"{self.email_label.text()}\n"
                )
            self.statusBar().showMessage(f"Saved: {os.path.basename(filename)}", 3000)

    def copy_card(self):
        pyperclip.copy(
            f"{self.name_label.text()}\n"
            f"{self.age_label.text()}\n"
            f"{self.position_label.text()}\n"
            f"{self.email_label.text()}"
        )
        self.statusBar().showMessage("Card copied to clipboard", 3000)

    def create_menu(self):
        file_menu = self.menuBar().addMenu("File")

        gen = QAction("Generate Card", self)
        gen.triggered.connect(self.update_display)
        file_menu.addAction(gen)

        save = QAction("Save Card", self)
        save.triggered.connect(self.save_card)
        file_menu.addAction(save)

        clear_disp = QAction("Clear Display", self)
        clear_disp.triggered.connect(self.clear_display)
        file_menu.addAction(clear_disp)

        exit_ac = QAction("Exit", self)
        exit_ac.triggered.connect(sys.exit)
        file_menu.addAction(exit_ac)

        edit_menu = self.menuBar().addMenu("Edit")

        copy = QAction("Copy Card", self)
        copy.triggered.connect(self.copy_card)
        edit_menu.addAction(copy)

        clear_form = QAction("Clear Form", self)
        clear_form.triggered.connect(self.clear_form)
        edit_menu.addAction(clear_form)

        # Rainbow option in Edit menu
        rainbow = QAction("🌈 Rainbow Background", self)
        rainbow.triggered.connect(self.set_rainbow_bg)
        edit_menu.addAction(rainbow)

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        gen = QAction(self.style().standardIcon(QStyle.SP_DialogApplyButton), "Generate", self)
        gen.triggered.connect(self.update_display)
        toolbar.addAction(gen)

        save = QAction(self.style().standardIcon(QStyle.SP_FileDialogNewFolder), "Save", self)
        save.triggered.connect(self.save_card)
        toolbar.addAction(save)

        clear = QAction(self.style().standardIcon(QStyle.SP_TrashIcon), "Clear All", self)
        clear.triggered.connect(self.clear_all)
        toolbar.addAction(clear)

        # Rainbow button in toolbar
        rainbow = QAction(self.style().standardIcon(QStyle.SP_TitleBarContextHelpButton), "Clear All", self)
        rainbow.setToolTip("Rainbow Background")
        rainbow.triggered.connect(self.set_rainbow_bg)
        toolbar.addAction(rainbow)


def main():
    sys.argv += ['-platform', 'windows:darkmode=1']
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = PersonalCard()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()