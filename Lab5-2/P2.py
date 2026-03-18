import sys
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel
)
from PySide6.QtCore import Qt


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(300, 450)
        self.expression = ""
        self._setup_ui()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(4)

        # Title
        title = QLabel("Standard")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        # Display
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setPlaceholderText("0")
        self.display.setStyleSheet("font-size: 28px; border: none; padding: 4px;")
        self.display.setFixedHeight(60)
        layout.addWidget(self.display)

        # Grid
        grid = QGridLayout()
        grid.setSpacing(4)

        def create_button(text):
            btn = QPushButton(text)
            btn.setFixedHeight(52)
            btn.setStyleSheet("font-size: 14px;")
            btn.clicked.connect(lambda _, t=text: self._on_button(t))
            return btn

        grid.addWidget(create_button("%"),    1, 0)
        grid.addWidget(create_button("CE"),   1, 1)
        grid.addWidget(create_button("C"),    1, 2)
        grid.addWidget(create_button("⌫"),    1, 3)

        grid.addWidget(create_button("¹/ₓ"),  2, 0)
        grid.addWidget(create_button("x²"),   2, 1)
        grid.addWidget(create_button("²√x"),  2, 2)
        grid.addWidget(create_button("÷"),    2, 3)

        grid.addWidget(create_button("7"),    3, 0)
        grid.addWidget(create_button("8"),    3, 1)
        grid.addWidget(create_button("9"),    3, 2)
        grid.addWidget(create_button("×"),    3, 3)

        grid.addWidget(create_button("4"),    4, 0)
        grid.addWidget(create_button("5"),    4, 1)
        grid.addWidget(create_button("6"),    4, 2)
        grid.addWidget(create_button("−"),    4, 3)

        grid.addWidget(create_button("1"),    5, 0)
        grid.addWidget(create_button("2"),    5, 1)
        grid.addWidget(create_button("3"),    5, 2)
        grid.addWidget(create_button("+"),    5, 3)

        grid.addWidget(create_button("+/-"),  6, 0)
        grid.addWidget(create_button("0"),    6, 1)
        grid.addWidget(create_button("."),    6, 2)

        btn_equal = create_button("=")
        btn_equal.setStyleSheet("font-size: 14px; background-color: #0078D4; color: white;")
        grid.addWidget(btn_equal, 6, 3)

        layout.addLayout(grid)

    def _on_button(self, text):
        if text in ("C", "CE"):
            self.expression = ""
            self.display.setText("")

        elif text == "⌫":
            self.expression = self.expression[:-1]
            self.display.setText(self.expression)

        elif text == "=":
            self._evaluate()

        elif text == "¹/ₓ":
            self._apply_unary(lambda v: 1 / v)

        elif text == "x²":
            self._apply_unary(lambda v: v ** 2)

        elif text == "²√x":
            self._apply_unary(lambda v: math.sqrt(v))

        elif text == "+/-":
            self._negate()

        elif text == "%":
            self.expression += "%"
            self.display.setText(self.expression)

        else:
            # Map display symbols to eval-compatible operators
            token = {"×": "*", "÷": "/", "−": "-"}.get(text, text)
            self.expression += token
            self.display.setText(self.expression)

    def _apply_unary(self, func):
        try:
            val = float(eval(self.expression))
            result = func(val)
            result = int(result) if result == int(result) else result
            self.expression = str(result)
            self.display.setText(self.expression)
        except ZeroDivisionError:
            self.display.setText("Cannot divide by 0")
            self.expression = ""
        except Exception:
            self.display.setText("Error")
            self.expression = ""

    def _negate(self):
        try:
            val = float(eval(self.expression))
            result = -val
            result = int(result) if result == int(result) else result
            self.expression = str(result)
            self.display.setText(self.expression)
        except Exception:
            self.display.setText("Error")
            self.expression = ""

    def _evaluate(self):
        try:
            result = eval(self.expression)
            result = int(result) if isinstance(result, float) and result == int(result) else result
            self.display.setText(str(result))
            self.expression = str(result)
        except ZeroDivisionError:
            self.display.setText("Cannot divide by 0")
            self.expression = ""
        except Exception:
            self.display.setText("Error")
            self.expression = ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Calculator()
    win.show()
    sys.exit(app.exec())