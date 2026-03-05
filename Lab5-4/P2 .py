import sys
import pyperclip
import random
from PySide6.QtWidgets import (QApplication, QMainWindow,
                                QVBoxLayout, QWidget, QHBoxLayout,
                                QGridLayout, QFormLayout, QLineEdit,
                                QLabel, QPushButton, QButtonGroup,
                                QRadioButton, QDateEdit, QComboBox,
                                QCheckBox, QTextEdit, QGroupBox,
                                QMessageBox, QTableWidget, QTableWidgetItem, 
                                QSpinBox, QMenu, QMenuBar, QStatusBar, 
                                QToolBar, QColorDialog, QFrame,
                                QFileDialog, QSlider)

from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QPixmap, QFont, QIcon, QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P2: Game Character Builder")
        self.setGeometry(100, 100, 850, 500)

        self.cantal_widget = CharacterBuilder()
        self.setCentralWidget(self.cantal_widget)

        self.setStyleSheet("""
            QToolBar {
                background-color: rgba(147, 162, 229, 40);
            }
            QStatusBar {
                background-color: rgba(147, 162, 229, 40)
            }
        """)

        #========= MENU =========
        self.menu = self.menuBar()

        game_menu = self.menu.addMenu("&Game")
        new_action = QAction("&New Character", self)
        new_action.triggered.connect(self.new_character)
        game_menu.addAction(new_action)

        generate_action = QAction("G&enerate Sheet", self)
        generate_action.triggered.connect(self.generate_sheet)
        game_menu.addAction(generate_action)

        save_action = QAction("&Save Sheet", self)
        save_action.triggered.connect(self.save_sheet)
        game_menu.addAction(save_action)

        game_menu.addSeparator()

        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(self.close)
        game_menu.addAction(exit_action)

        edit_menu = self.menu.addMenu("E&dit")
        reset_action = QAction("Reset Stats", self)
        reset_action.triggered.connect(self.reset_stats)
        edit_menu.addAction(reset_action)

        random_action = QAction("Randomize", self)
        random_action.triggered.connect(self.randomize)
        edit_menu.addAction(random_action)

        #========== Tool =========
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        new_tool = QAction("📙 New", self)
        new_tool.setToolTip("New Character")
        new_tool.triggered.connect(self.new_character)
        toolbar.addAction(new_tool)

        generate_tool = QAction("⚔️ Generate", self)
        generate_tool.setToolTip("Generate Sheet")
        generate_tool.triggered.connect(self.generate_sheet)
        toolbar.addAction(generate_tool)

        random_tool = QAction("🎲 Randomize", self)
        random_tool.setToolTip("Randomize Sheet")
        random_tool.triggered.connect(self.randomize)
        toolbar.addAction(random_tool)

        save_tool = QAction("💾 Save", self)
        save_tool.setToolTip("Save Sheet")
        save_tool.triggered.connect(self.save_sheet)
        toolbar.addAction(save_tool)

        #========== Status ========
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready —— create your character")
        self.status.addPermanentWidget(QLabel("Created by Tintrai."))

    def show_status(self, msg, color="black"):
        self.status.setStyleSheet(f"color: {color};")
        self.status.showMessage(msg, 3000)

    def new_character(self):
        c = self.cantal_widget
        c.name_input.clear()
        c.race_input.setCurrentIndex(-1)
        c.class_input.setCurrentIndex(-1)
        c.gender_input.setCurrentIndex(-1)

        c.str_input_sild.setValue(5)
        c.dex_input_sild.setValue(5)
        c.int_input_sild.setValue(5)
        c.vit_input_sild.setValue(5)

        c.str_input_value.setText(str(c.str_input_sild.value()))
        c.dex_input_value.setText(str(c.dex_input_sild.value()))
        c.int_input_value.setText(str(c.int_input_sild.value()))
        c.vit_input_value.setText(str(c.vit_input_sild.value()))

        c.updateCard()

        self.show_status("New character — all fields reset.")
    
    def generate_sheet(self):
        c = self.cantal_widget
        c.updateCard()
        self.show_status("Generate.")
    
    def save_sheet(self):
        c = self.cantal_widget
        name = c.name_input.text().strip()
        if not name:
            self.show_status("⚠️ Enter a name before saving.", "red")
            QMessageBox.warning(self, "Error", "Please enter a character name first.")
            return

        s = c.str_input_sild.value()
        d = c.dex_input_sild.value()
        i = c.int_input_sild.value()
        v = c.vit_input_sild.value()

        sheet = (
            f"=== CHARACTER SHEET ===\n"
            f"Name  : {name}\n"
            f"Race  : {c.race_input.currentText()}\n"
            f"Class : {c.class_input.currentText()}\n"
            f"Gender: {c.gender_input.currentText()}\n"
            f"\n--- STATS ---\n"
            f"STR : {s}\n"
            f"DEX : {d}\n"
            f"INT : {i}\n"
            f"VIT : {v}\n"
            f"Total: {s+d+i+v}/40\n"
        )

        path, _ = QFileDialog.getSaveFileName(
            self, "Save Character Sheet", f"{name}.txt", "Text Files (*.txt)"
        )
        if path:
            with open(path, "w") as f:
                f.write(sheet)
            self.show_status("💾 Saved!", "green")
        else:
            self.show_status("Save cancelled.")

    def reset_stats(self):
        c = self.cantal_widget
        for sld in [c.str_input_sild, c.dex_input_sild,
                    c.int_input_sild, c.vit_input_sild]:
            sld.setValue(5)
        self.show_status("🔄 Stats reset to 5.")
    
    def randomize(self):
        c = self.cantal_widget

        c.race_input.setCurrentIndex(random.randint(0, c.race_input.count() - 1))
        c.class_input.setCurrentIndex(random.randint(0, c.class_input.count() - 1))
        c.gender_input.setCurrentIndex(random.randint(0, c.gender_input.count() - 1))

        names = ["Arion", "Lyra", "Drak", "Seraph", "Voss", "Elowen", "Thane", "Mira"]
        c.name_input.setText(random.choice(names))

        # สุ่ม stats รวม ≤ 40 แต่ละตัว 1–20
        sliders = [c.str_input_sild, c.dex_input_sild,
                   c.int_input_sild, c.vit_input_sild]
        budget = 40
        vals = []
        for idx in range(len(sliders)):
            remaining = len(sliders) - idx - 1
            hi = min(20, budget - remaining)
            hi = max(1, hi)
            val = random.randint(1, hi)
            vals.append(val)
            budget -= val

        for sld, val in zip(sliders, vals):
            sld.blockSignals(True)
            sld.setValue(val)
            sld.blockSignals(False)

        c.cal_point()
        self.show_status("🎲 Character randomized!", "blue")

class CharacterBuilder(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        
        left_widget = QWidget()
        layout = QVBoxLayout()
        left_widget.setLayout(layout)
        main_layout.addWidget(left_widget)

        self.card = CharacterCard()
        main_layout.addWidget(self.card, alignment=Qt.AlignTop)

        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel("Character Name:"), alignment=Qt.AlignLeft)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter character name")
        layout1.addWidget(self.name_input, alignment=Qt.AlignRight)
        layout.addLayout(layout1)

        layout2 = QHBoxLayout()
        layout2.addWidget(QLabel("Race:"))
        self.race_input = QComboBox()
        self.race_input.setPlaceholderText("Choose race")
        self.race_input.addItems(["Human", "Elf", "Dwarf", "Orc", "Undead"])
        layout2.addWidget(self.race_input)
        layout.addLayout(layout2)

        layout3 = QHBoxLayout()
        layout3.addWidget(QLabel("Class:"))
        self.class_input = QComboBox()
        self.class_input.setPlaceholderText("Choose class")
        self.class_input.addItems(["Warrior", "Mage", "Rogue", "Paladin", "Ranger"])
        layout3.addWidget(self.class_input)
        layout.addLayout(layout3)

        layout4 = QHBoxLayout()
        layout4.addWidget(QLabel("Gender:"))
        self.gender_input = QComboBox()
        self.gender_input.setPlaceholderText("Choose gender")
        self.gender_input.addItems(["Male", "Female", "Other"])
        layout4.addWidget(self.gender_input)
        layout.addLayout(layout4)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setLineWidth(1)
        layout.addWidget(line)

        stat = QLabel("Stat Allocation")
        stat.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(stat)

        layout5 = QHBoxLayout()
        layout5.addWidget(QLabel("⚔️ STR"))
        self.str_input_sild = QSlider(Qt.Horizontal)
        self.str_input_sild.setFixedWidth(400)
        self.str_input_sild.setMinimum(1)
        self.str_input_sild.setMaximum(20)
        self.str_input_sild.setValue(5)
        layout5.addWidget(self.str_input_sild)
        self.str_input_value = QLabel("5")
        layout5.addWidget(self.str_input_value)
        self.str_input_sild.valueChanged.connect(self.cal_point)
        layout.addLayout(layout5)

        layout6 = QHBoxLayout()
        layout6.addWidget(QLabel("🏃 DEX"))
        self.dex_input_sild = QSlider(Qt.Horizontal)
        self.dex_input_sild.setFixedWidth(400)
        self.dex_input_sild.setMinimum(1)
        self.dex_input_sild.setMaximum(20)
        self.dex_input_sild.setValue(5)
        layout6.addWidget(self.dex_input_sild)
        self.dex_input_value = QLabel("5")
        layout6.addWidget(self.dex_input_value)
        self.dex_input_sild.valueChanged.connect(self.cal_point)
        layout.addLayout(layout6)

        layout7 = QHBoxLayout()
        layout7.addWidget(QLabel("🔮 INT"))
        self.int_input_sild = QSlider(Qt.Horizontal)
        self.int_input_sild.setFixedWidth(400)
        self.int_input_sild.setMinimum(1)
        self.int_input_sild.setMaximum(20)
        self.int_input_sild.setValue(5)
        layout7.addWidget(self.int_input_sild)
        self.int_input_value = QLabel("5")
        layout7.addWidget(self.int_input_value)
        self.int_input_sild.valueChanged.connect(self.cal_point)
        layout.addLayout(layout7)

        layout8 = QHBoxLayout()
        layout8.addWidget(QLabel("❤️ VIT"))
        self.vit_input_sild = QSlider(Qt.Horizontal)
        self.vit_input_sild.setFixedWidth(400)
        self.vit_input_sild.setMinimum(1)
        self.vit_input_sild.setMaximum(20)
        self.vit_input_sild.setValue(5)
        layout8.addWidget(self.vit_input_sild)
        self.vit_input_value = QLabel("5")
        layout8.addWidget(self.vit_input_value)
        self.vit_input_sild.valueChanged.connect(self.cal_point)
        layout.addLayout(layout8)

        self.point = QLabel("Point used: 20/40")
        self.point.setFont(QFont("Arial", 8, QFont.Bold))
        layout.addWidget(self.point, alignment=Qt.AlignLeft)

        gen_btn = QPushButton("⚔️ Generate Character Sheet")
        gen_btn.setStyleSheet("background-color: rgba(147, 162, 229, 40); color: green; border: 1px solid; border-color: green;")
        gen_btn.clicked.connect(self.updateCard)
        layout.addWidget(gen_btn)

        layout.addStretch()

    def cal_point(self):
        total = (self.str_input_sild.value() + self.dex_input_sild.value()
                 + self.int_input_sild.value() + self.vit_input_sild.value())

        if total > 40:
            sender = self.sender()
            if sender:
                excess = total - 40
                sender.blockSignals(True)
                sender.setValue(sender.value() - excess)
                sender.blockSignals(False)
                total = (self.str_input_sild.value() + self.dex_input_sild.value()
                         + self.int_input_sild.value() + self.vit_input_sild.value())
        
        self.str_input_value.setText(str(self.str_input_sild.value()))
        self.dex_input_value.setText(str(self.dex_input_sild.value()))
        self.int_input_value.setText(str(self.int_input_sild.value()))
        self.vit_input_value.setText(str(self.vit_input_sild.value()))
        self.point.setText(f"Point used: {total}/40")

        self.update_color(total)

    def updateCard(self):
        name = self.name_input.text()
        race_out = self.race_input.currentText()
        class_out = self.class_input.currentText()

        if not name:
            name = "Character Name"
        if not race_out or not class_out:
            race_out = "Race"
            class_out = "Class"

        self.card.name.setText(f"—— {name.strip()} ——")
        self.card.race_class.setText(f"{race_out} • {class_out}")

        # bar width: max value 20 -> max fill 200px  (1 point = 10px)
        s_val = self.str_input_sild.value()
        self.card.str_bar_fill.setFixedWidth(s_val * 10)
        self.card.str_val_lbl.setText(str(s_val))

        d_val = self.dex_input_sild.value()
        self.card.dex_bar_fill.setFixedWidth(d_val * 10)
        self.card.dex_val_lbl.setText(str(d_val))

        i_val = self.int_input_sild.value()
        self.card.int_bar_fill.setFixedWidth(i_val * 10)
        self.card.int_val_lbl.setText(str(i_val))

        v_val = self.vit_input_sild.value()
        self.card.vit_bar_fill.setFixedWidth(v_val * 10)
        self.card.vit_val_lbl.setText(str(v_val))

    def update_color(self, total: int):
        self.str_input_value.setText(str(self.str_input_sild.value()))
        self.dex_input_value.setText(str(self.dex_input_sild.value()))
        self.int_input_value.setText(str(self.int_input_sild.value()))
        self.vit_input_value.setText(str(self.vit_input_sild.value()))

        color = "red" if total > 40 else "black"
        self.point.setStyleSheet(f"color: {color};")
        self.point.setText(f"Point used: {total}/40")

class CharacterCard(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setFixedSize(250,500)
        self.setAttribute(Qt.WA_StyledBackground, True) 
        self.setAutoFillBackground(True) 
        layout.setSpacing(15)

        self.setStyleSheet("""
            QWidget {
                background-color: #2a2d45;
                border-radius: 12px;
            }
            QLabel {
                color: #dde0f0;
                background: transparent;     /* ป้องกัน label ทับ bg */
            }
            QFrame#bg {
                background-color: #3a3f5c;
                border: 1px solid #4a5070;
                border-radius: 2px;
            }
            QFrame#fill {
                background-color: #7b82c8;
                border-radius: 2px;
            }
        """)
        

        self.name = QLabel("—— Character Name ——")
        layout.addWidget(self.name, alignment=Qt.AlignCenter)

        self.race_class = QLabel("Race • Class")
        layout.addWidget(self.race_class, alignment=Qt.AlignCenter)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setLineWidth(1)
        layout.addWidget(line)

        # STR Bar
        lay1 = QHBoxLayout()
        lay1.addWidget(QLabel("STR"))
        bg1 = QFrame()
        bg1.setFixedSize(200, 12)
        bg1.setObjectName("bg")
        self.str_bar_fill = QFrame(bg1)
        self.str_bar_fill.setFixedSize(0, 12)
        self.str_bar_fill.setObjectName("fill")
        lay1.addWidget(bg1)
        self.str_val_lbl = QLabel("—")
        lay1.addWidget(self.str_val_lbl)
        layout.addLayout(lay1)

        # DEX Bar
        lay2 = QHBoxLayout()
        lay2.addWidget(QLabel("DEX"))
        bg2 = QFrame()
        bg2.setFixedSize(200, 12)
        bg2.setObjectName("bg")
        self.dex_bar_fill = QFrame(bg2)
        self.dex_bar_fill.setFixedSize(0, 12)
        self.dex_bar_fill.setObjectName("fill")
        lay2.addWidget(bg2)
        self.dex_val_lbl = QLabel("—")
        lay2.addWidget(self.dex_val_lbl)
        layout.addLayout(lay2)

        # INT Bar
        lay3 = QHBoxLayout()
        lay3.addWidget(QLabel("INT"))
        bg3 = QFrame()
        bg3.setFixedSize(200, 12)
        bg3.setObjectName("bg")
        self.int_bar_fill = QFrame(bg3)
        self.int_bar_fill.setFixedSize(0, 12)
        self.int_bar_fill.setObjectName("fill")
        lay3.addWidget(bg3)
        self.int_val_lbl = QLabel("—")
        lay3.addWidget(self.int_val_lbl)
        layout.addLayout(lay3)

        # VIT Bar
        lay4 = QHBoxLayout()
        lay4.addWidget(QLabel("VIT"))
        bg4 = QFrame()
        bg4.setFixedSize(200, 12)
        bg4.setObjectName("bg")
        self.vit_bar_fill = QFrame(bg4)
        self.vit_bar_fill.setFixedSize(0, 12)
        self.vit_bar_fill.setObjectName("fill")
        lay4.addWidget(bg4)
        self.vit_val_lbl = QLabel("—")
        lay4.addWidget(self.vit_val_lbl)
        layout.addLayout(lay4)

        layout.addStretch()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())