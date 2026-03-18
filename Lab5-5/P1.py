import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QLineEdit, QDateEdit, QSpinBox,
    QPushButton, QDialog, QMessageBox, QScrollArea,
    QFrame, QSizePolicy, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QDate, QRegularExpression
from PySide6.QtGui import QFont, QColor, QRegularExpressionValidator

# ── Palette ───────────────────────────────────────────────────────────────
BG        = "#F7F4EF"
PANEL     = "#FFFFFF"
BORDER    = "#E8E0D4"
ACCENT    = "#2C6E6A"
ACCENT_HV = "#1F4E4B"
GOLD      = "#C8965A"
TEXT_PRI  = "#1C1A17"
TEXT_SEC  = "#7A7060"
SEL_BG    = "#EAF4F3"

def _shadow(widget, radius=12, opacity=28):
    eff = QGraphicsDropShadowEffect()
    eff.setBlurRadius(radius)
    eff.setOffset(0, 3)
    eff.setColor(QColor(0, 0, 0, opacity))
    widget.setGraphicsEffect(eff)
    return widget

HERO_STYLE = f"""
    QFrame {{
        background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
            stop:0 {ACCENT}, stop:1 #3D8F8A);
        border-radius: 14px;
    }}
"""

INPUT_STYLE = f"""
    QLineEdit, QDateEdit, QSpinBox {{
        border: 1.5px solid {BORDER};
        border-radius: 6px;
        padding: 8px 10px;
        background: {PANEL};
        color: {TEXT_PRI};
        font-size: 12px;
        font-family: 'Trebuchet MS';
    }}
    QLineEdit:focus, QDateEdit:focus, QSpinBox:focus {{
        border: 1.5px solid {ACCENT};
        background: {SEL_BG};
    }}
"""


# ─────────────────────────────────────────────
#  Custom Widget: RoomCard
# ─────────────────────────────────────────────
class RoomCard(QWidget):
    """
    Room information card — Custom Widget Class
    Practice:
      - Inheriting QWidget
      - Signal to pass data to parent
      - select() / deselect() methods to change visual state
    """

    # Signal: emits (room_name, price) when user clicks Select
    room_selected = Signal(str, int)

    def __init__(self, room_name: str, price: int, description: str, emoji: str = "🏨"):
        super().__init__()
        self._is_selected = False
        self._room_name = room_name
        self._price = price

        self._build_ui(emoji, room_name, price, description)
        self.deselect()  # Set default style

    def _build_ui(self, emoji: str, room_name: str, price: int, description: str):
        self.setFixedSize(188, 220)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 18, 14, 14)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Create labels and button in the card
        icon_lbl = QLabel(emoji)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setFont(QFont("Segoe UI Emoji", 30))
        icon_lbl.setStyleSheet("background: transparent;")

        name_lbl = QLabel(room_name)
        name_lbl.setAlignment(Qt.AlignCenter)
        name_lbl.setFont(QFont("Georgia", 11, QFont.Bold))
        name_lbl.setStyleSheet(f"color: {TEXT_PRI}; background: transparent;")

        price_row = QHBoxLayout()
        price_row.setAlignment(Qt.AlignCenter)
        price_main = QLabel(f"${price}")
        price_main.setFont(QFont("Georgia", 14, QFont.Bold))
        price_main.setStyleSheet(f"color: {GOLD}; background: transparent;")
        price_night = QLabel("/ night")
        price_night.setFont(QFont("Trebuchet MS", 9))
        price_night.setStyleSheet(f"color: {TEXT_SEC}; background: transparent;")
        price_row.addWidget(price_main)
        price_row.addWidget(price_night)

        desc_lbl = QLabel(description)
        desc_lbl.setAlignment(Qt.AlignCenter)
        desc_lbl.setWordWrap(True)
        desc_lbl.setFont(QFont("Trebuchet MS", 9))
        desc_lbl.setStyleSheet(f"color: {TEXT_SEC}; background: transparent;")

        self.select_btn = QPushButton("Select Room")
        self.select_btn.setFixedHeight(34)
        self.select_btn.setCursor(Qt.PointingHandCursor)
        self.select_btn.clicked.connect(self._on_select_clicked)

        # Add labels and button to the layout
        layout.addWidget(icon_lbl)
        layout.addWidget(name_lbl)
        layout.addLayout(price_row)
        layout.addWidget(desc_lbl)
        layout.addStretch()
        layout.addWidget(self.select_btn)

    def _on_select_clicked(self):
        """When button is clicked, emit signal to notify parent"""
        self.room_selected.emit(self._room_name, self._price)

    def select(self):
        """Change to selected state"""
        self._is_selected = True
        self.setStyleSheet(f"""
            RoomCard {{
                border: 2px solid {ACCENT};
                border-radius: 12px;
                background: {SEL_BG};
            }}
        """)
        self.select_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT}; color: white;
                border-radius: 7px; font-weight: bold;
                font-family: 'Trebuchet MS'; font-size: 12px;
            }}
        """)
        self.select_btn.setText("✓  Selected")

    def deselect(self):
        """Change back to normal state"""
        self._is_selected = False
        self.setStyleSheet(f"""
            RoomCard {{
                border: 1.5px solid {BORDER};
                border-radius: 12px;
                background: {PANEL};
            }}
        """)
        self.select_btn.setStyleSheet(f"""
            QPushButton {{
                background: {PANEL}; color: {ACCENT};
                border: 1.5px solid {ACCENT};
                border-radius: 7px;
                font-family: 'Trebuchet MS'; font-size: 12px;
            }}
            QPushButton:hover {{
                background: {ACCENT}; color: white;
            }}
        """)
        self.select_btn.setText("Select Room")

    def is_selected(self):
        return self._is_selected


# ─────────────────────────────────────────────
#  Custom Dialog: ConfirmDialog
# ─────────────────────────────────────────────
class ConfirmDialog(QDialog):
    """
    Booking confirmation popup — Custom Dialog Class
    Practice:
      - Inheriting QDialog
      - Building layout and widgets inside the dialog manually
    """

    def __init__(self, guest_name: str, room_name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Booking Confirmed")
        self.setFixedSize(360, 230)
        self.setModal(True)
        self.setStyleSheet(f"background: {PANEL};")
        self._build_ui(guest_name, room_name)

    def _build_ui(self, guest_name: str, room_name: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 28, 30, 28)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignCenter)

        # Create labels and button in the card
        check_lbl = QLabel("✅")
        check_lbl.setAlignment(Qt.AlignCenter)
        check_lbl.setFont(QFont("Segoe UI Emoji", 38))
        check_lbl.setStyleSheet("background: transparent;")

        title_lbl = QLabel("Booking Successful!")
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setFont(QFont("Georgia", 17, QFont.Bold))
        title_lbl.setStyleSheet(f"color: {ACCENT}; background: transparent;")

        msg_lbl = QLabel(f"Dear {guest_name},\n{room_name} is ready to welcome you! 🎉")
        msg_lbl.setAlignment(Qt.AlignCenter)
        msg_lbl.setWordWrap(True)
        msg_lbl.setFont(QFont("Trebuchet MS", 10))
        msg_lbl.setStyleSheet(f"color: {TEXT_SEC}; background: transparent;")

        ok_btn = QPushButton("OK")
        ok_btn.setFixedHeight(42)
        ok_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT}; color: white;
                border-radius: 9px;
                font-family: 'Georgia'; font-size: 14px; font-weight: bold;
            }}
            QPushButton:hover {{ background: {ACCENT_HV}; }}
        """)
        ok_btn.clicked.connect(self.accept)

        # Add labels and button to the layout
        layout.addWidget(check_lbl)
        layout.addWidget(title_lbl)
        layout.addWidget(msg_lbl)
        layout.addWidget(ok_btn)


# ─────────────────────────────────────────────
#  Page 1: BookingPage
# ─────────────────────────────────────────────
class BookingPage(QWidget):
    """
    Page 1 — Guest information form and room selection
    """

    def __init__(self):
        super().__init__()
        self.selected_room = None
        self.selected_price = 0
        self.cards = []  # a list of RoomCard objects
        self._build_ui()

    def _build_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet(f"QScrollArea {{ background: {BG}; border: none; }}")

        container = QWidget()
        container.setStyleSheet(f"background: {BG};")
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(30, 24, 30, 24)
        main_layout.setSpacing(16)

        # ── Hero header ──
        hero = QFrame()
        hero.setStyleSheet(HERO_STYLE)
        _shadow(hero, 20, 40)
        hl = QVBoxLayout(hero)
        hl.setContentsMargins(28, 20, 28, 20)
        title = QLabel("🏨  Book Your Stay at CozyStay")
        title.setFont(QFont("Georgia", 20, QFont.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        subtitle = QLabel("Fill in your details and choose your room")
        subtitle.setFont(QFont("Trebuchet MS", 10))
        subtitle.setStyleSheet("color: rgba(255,255,255,0.75); background: transparent;")
        hl.addWidget(title)
        hl.addWidget(subtitle)
        main_layout.addWidget(hero)

        # ── Section 1: Guest Info Form ──
        form_title = QLabel("📋  Guest Information")
        form_title.setFont(QFont("Georgia", 13, QFont.Bold))
        form_title.setStyleSheet(f"color: {ACCENT}; background: transparent;")
        main_layout.addWidget(form_title)

        form_frame = QFrame()
        form_frame.setStyleSheet(f"""
            QFrame {{
                background: {PANEL};
                border: 1.5px solid {BORDER};
                border-radius: 12px;
            }}
            {INPUT_STYLE}
        """)
        _shadow(form_frame)

        # Create widgets for inputs
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter name")
        # Full Name: letters, spaces, dots, hyphens only — no digits
        self.name_input.setValidator(
            QRegularExpressionValidator(QRegularExpression(r"[^\d]+")))

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter Phone Number")
        # Phone: digits and hyphens only — no letters
        self.phone_input.setValidator(
            QRegularExpressionValidator(QRegularExpression(r"[\d\-]+")))

        self.checkin_input = QDateEdit(QDate.currentDate())
        self.checkin_input.setDisplayFormat("dd/MM/yyyy")
        self.checkin_input.setCalendarPopup(True)

        self.checkout_input = QDateEdit(QDate.currentDate().addDays(1))
        self.checkout_input.setDisplayFormat("dd/MM/yyyy")
        self.checkout_input.setCalendarPopup(True)

        self.guests_input = QSpinBox()
        self.guests_input.setRange(1, 10)
        self.guests_input.setValue(1)
        self.guests_input.setSuffix(" guest(s)")

        # Set style for inputs and their labels
        for w in [self.name_input, self.phone_input,
                  self.checkin_input, self.checkout_input, self.guests_input]:
            w.setMinimumWidth(200)

        label_style = f"font-size: 12px; color: {TEXT_PRI}; font-weight: bold; font-family: Georgia; background: transparent;"

        grid = QGridLayout(form_frame)
        grid.setContentsMargins(24, 20, 24, 20)
        grid.setVerticalSpacing(14)
        grid.setHorizontalSpacing(16)
        grid.setColumnStretch(1, 1)

        for i, (text, widget) in enumerate([
            ("Full Name :",      self.name_input),
            ("Phone Number :",   self.phone_input),
            ("Check-in Date :",  self.checkin_input),
            ("Check-out Date :", self.checkout_input),
            ("Guests :",         self.guests_input),
        ]):
            lbl = QLabel(text)
            lbl.setStyleSheet(label_style)
            lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            lbl.setFixedWidth(126)
            grid.addWidget(lbl, i, 0)
            grid.addWidget(widget, i, 1)

        main_layout.addWidget(form_frame)

        # ── Section 2: Room Selection ──
        room_title = QLabel("🛏️  Select a Room")
        room_title.setFont(QFont("Georgia", 13, QFont.Bold))
        room_title.setStyleSheet(f"color: {ACCENT}; background: transparent;")
        main_layout.addWidget(room_title)

        rooms_data = [
            ("Standard Room", 50,  "Single bed · Free Wi-Fi",             "🛏️"),
            ("Deluxe Room",   120, "Double bed · Ocean view · Wi-Fi",     "🌊"),
            ("Suite Room",    250, "Living room · Jacuzzi · Premium view","👑"),
            ("Family Room",   160, "2 Bedrooms · Perfect for families",   "👨‍👩‍👧‍👦"),
        ]

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(14)
        cards_layout.setContentsMargins(0, 0, 0, 0)

        # Create cards according to the info above
        for room_name, price, desc, emoji in rooms_data:
            card = RoomCard(room_name, price, desc, emoji)
            _shadow(card, 10, 18)
            # catch the emitted signal from each card
            card.room_selected.connect(self._on_room_selected)
            self.cards.append(card)
            cards_layout.addWidget(card)

        cards_layout.addStretch()
        main_layout.addLayout(cards_layout)

        # ── Divider ──
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {BORDER};")
        main_layout.addWidget(line)

        # ── Buttons ──
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.clear_btn = QPushButton("🗑  Clear Info")
        self.clear_btn.setFixedSize(120, 38)
        self.clear_btn.setFont(QFont("Trebuchet MS", 11))
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.setStyleSheet(f"""
            QPushButton {{
                background: {PANEL}; color: {TEXT_SEC};
                border: 1.5px solid {BORDER}; border-radius: 8px;
            }}
            QPushButton:hover {{ background: #F0EBE3; color: {TEXT_PRI}; }}
        """)
        # Connect the button's signal to a slot
        self.clear_btn.clicked.connect(self.clear_form)

        self.next_btn = QPushButton("Next  →")
        self.next_btn.setFixedSize(130, 38)
        self.next_btn.setFont(QFont("Georgia", 11, QFont.Bold))
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT}; color: white;
                border: none; border-radius: 8px;
            }}
            QPushButton:hover {{ background: {ACCENT_HV}; }}
        """)

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.next_btn)

        main_layout.addLayout(btn_layout)
        main_layout.addStretch()

        scroll.setWidget(container)

        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)

    def _on_room_selected(self, room_name: str, price: int):
        """Receive signal from RoomCard, update state, deselect other cards"""
        self.selected_room = room_name
        self.selected_price = price
        for card in self.cards:
            if card._room_name == room_name:
                card.select()
            else:
                card.deselect()

    def clear_form(self):
        """Clear all form fields and deselect all room cards"""
        self.name_input.clear()
        self.phone_input.clear()
        self.checkin_input.setDate(QDate.currentDate())
        self.checkout_input.setDate(QDate.currentDate().addDays(1))
        self.guests_input.setValue(1)
        self.selected_room = None
        self.selected_price = 0
        for card in self.cards:
            card.deselect()

    def get_booking_data(self):
        """Collect form data — returns None if validation fails"""
        name    = self.name_input.text().strip()
        phone   = self.phone_input.text().strip()
        checkin  = self.checkin_input.date()
        checkout = self.checkout_input.date()

        if not name:
            QMessageBox.warning(self, "Missing Information", "Please enter your full name.")
            return None
        if not phone:
            QMessageBox.warning(self, "Missing Information", "Please enter your phone number.")
            return None
        if checkin >= checkout:
            QMessageBox.warning(self, "Invalid Dates",
                                "Check-out date must be after check-in date.")
            return None
        if not self.selected_room:
            QMessageBox.warning(self, "No Room Selected",
                                "Please select a room before proceeding.")
            return None

        nights = checkin.daysTo(checkout)
        total  = self.selected_price * nights

        data_dict = {
            "name":     name,
            "phone":    phone,
            "checkin":  checkin.toString("dd/MM/yyyy"),
            "checkout": checkout.toString("dd/MM/yyyy"),
            "guests":   self.guests_input.value(),
            "room":     self.selected_room,
            "price":    self.selected_price,
            "nights":   nights,
            "total":    total,
        }
        return data_dict


# ─────────────────────────────────────────────
#  Page 2: ReviewPage
# ─────────────────────────────────────────────
class ReviewPage(QWidget):
    """
    Page 2 — Review booking details before submitting
    """

    def __init__(self):
        super().__init__()
        self.current_data = {}
        self._build_ui()

    def _build_ui(self):
        self.setStyleSheet(f"background: {BG};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        # ── Hero header ──
        hero = QFrame()
        hero.setStyleSheet(HERO_STYLE)
        _shadow(hero, 20, 40)
        hl = QVBoxLayout(hero)
        hl.setContentsMargins(28, 20, 28, 20)
        title = QLabel("📋  Booking Summary")
        title.setFont(QFont("Georgia", 20, QFont.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        subtitle = QLabel("Please review your details before confirming")
        subtitle.setFont(QFont("Trebuchet MS", 10))
        subtitle.setStyleSheet("color: rgba(255,255,255,0.75); background: transparent;")
        hl.addWidget(title)
        hl.addWidget(subtitle)
        layout.addWidget(hero)

        # ── Info card ──
        self.info_frame = QFrame()
        self.info_frame.setStyleSheet(f"""
            QFrame {{
                background: {PANEL};
                border: 1.5px solid {BORDER};
                border-radius: 12px;
            }}
        """)
        _shadow(self.info_frame)

        self.info_layout = QGridLayout(self.info_frame)
        self.info_layout.setContentsMargins(28, 20, 28, 20)
        self.info_layout.setVerticalSpacing(12)
        self.info_layout.setHorizontalSpacing(20)
        self.info_layout.setColumnStretch(2, 1)

        display_data = [
            ("🛏️",  "Room",          ""),
            ("💲",  "Price / Night",  "$ -"),
            ("👤",  "Guest Name",     ""),
            ("📞",  "Phone",          ""),
            ("📅",  "Check-in",       ""),
            ("📅",  "Check-out",      ""),
            ("🌙",  "Nights",         "- night(s)"),
            ("👥",  "Guests",         "- guest(s)"),
        ]

        key_style = f"font-weight: bold; color: {TEXT_SEC}; font-size: 12px; font-family: 'Trebuchet MS'; background: transparent;"
        val_style = f"color: {TEXT_PRI}; font-size: 12px; font-family: Georgia; background: transparent;"

        self.val_labels = []
        grid_row = 0
        for i, (icon, key, placeholder) in enumerate(display_data):
            il = QLabel(icon)
            il.setFont(QFont("Segoe UI Emoji", 14))
            il.setAlignment(Qt.AlignCenter)
            il.setStyleSheet("background: transparent;")

            kl = QLabel(key)
            kl.setStyleSheet(key_style)
            kl.setFixedWidth(120)

            vl = QLabel(placeholder)
            vl.setStyleSheet(val_style)
            self.val_labels.append(vl)

            self.info_layout.addWidget(il, grid_row, 0)
            self.info_layout.addWidget(kl, grid_row, 1)
            self.info_layout.addWidget(vl, grid_row, 2)
            grid_row += 1

            if i < len(display_data) - 1:
                sep = QFrame()
                sep.setFrameShape(QFrame.HLine)
                sep.setStyleSheet(f"color: {BORDER};")
                self.info_layout.addWidget(sep, grid_row, 0, 1, 3)
                grid_row += 1

        layout.addWidget(self.info_frame)

        # ── Total banner ──
        total_banner = QFrame()
        total_banner.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #FFF8EE, stop:1 #FFF3E0);
                border: 1.5px solid {GOLD};
                border-radius: 10px;
            }}
        """)
        tl = QHBoxLayout(total_banner)
        tl.setContentsMargins(24, 14, 24, 14)
        tl.addStretch()
        ti = QLabel("💰")
        ti.setFont(QFont("Segoe UI Emoji", 16))
        ti.setStyleSheet("background: transparent;")
        tl.addWidget(ti)
        tl.addSpacing(8)
        self.total_label = QLabel("Total Amount :  $-")
        self.total_label.setFont(QFont("Georgia", 18, QFont.Bold))
        self.total_label.setStyleSheet(f"color: {GOLD}; background: transparent;")
        tl.addWidget(self.total_label)
        layout.addWidget(total_banner)

        layout.addStretch()

        # ── Divider ──
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {BORDER};")
        layout.addWidget(line)

        # ── Buttons ──
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.back_btn = QPushButton("←  Back")
        self.back_btn.setFixedSize(110, 38)
        self.back_btn.setFont(QFont("Trebuchet MS", 11))
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setStyleSheet(f"""
            QPushButton {{
                background: {PANEL}; color: {TEXT_SEC};
                border: 1.5px solid {BORDER}; border-radius: 8px;
            }}
            QPushButton:hover {{ background: #F0EBE3; color: {TEXT_PRI}; }}
        """)

        self.submit_btn = QPushButton("☑  Confirm Booking")
        self.submit_btn.setFixedSize(170, 38)
        self.submit_btn.setFont(QFont("Georgia", 11, QFont.Bold))
        self.submit_btn.setCursor(Qt.PointingHandCursor)
        self.submit_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT}; color: white;
                border: none; border-radius: 8px;
            }}
            QPushButton:hover {{ background: {ACCENT_HV}; }}
        """)

        btn_layout.addWidget(self.back_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.submit_btn)
        layout.addLayout(btn_layout)

    def load_data(self, data: dict):
        """Receive data dict from BookingPage and populate the review layout"""
        self.current_data = data

        # Set all values from data in appropriate labels
        values = [
            data["room"],
            f"${data['price']}",
            data["name"],
            data["phone"],
            data["checkin"],
            data["checkout"],
            f"{data['nights']} night(s)",
            f"{data['guests']} guest(s)",
        ]
        for lbl, val in zip(self.val_labels, values):
            lbl.setText(str(val))

        self.total_label.setText(f"Total Amount :  ${data['total']:,}")


# ─────────────────────────────────────────────
#  Main Window
# ─────────────────────────────────────────────
class MainWindow(QMainWindow):
    """
    Main window — uses QStackedWidget to manage 2 pages
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CozyStay — Hotel Booking System")
        self.setMinimumSize(820, 680)
        self.resize(900, 720)

        # QStackedWidget as central widget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Create pages
        self.booking_page = BookingPage()
        self.review_page  = ReviewPage()

        # Add to stack: index 0 = booking, index 1 = review
        self.stack.addWidget(self.booking_page)
        self.stack.addWidget(self.review_page)

        # Connect navigation
        self.booking_page.next_btn.clicked.connect(self._go_to_review)
        self.review_page.back_btn.clicked.connect(self._go_to_booking)
        self.review_page.submit_btn.clicked.connect(self._on_submit)

        # Start on page 0
        self.stack.setCurrentIndex(0)

        self.setStyleSheet(f"""
            QMainWindow {{ background: {BG}; }}
            QScrollArea  {{ background: transparent; }}
            QWidget      {{ font-family: 'Trebuchet MS', 'Segoe UI', sans-serif; }}
        """)

    def _go_to_review(self):
        """Validate form, then switch to Review page"""
        data = self.booking_page.get_booking_data()

        if data is None:
            return

        # Load data into the review page
        self.review_page.load_data(data)

        # Set stack index to the review page
        self.stack.setCurrentIndex(1)

    def _go_to_booking(self):
        """Go back to Booking page, form data remains intact"""
        self.stack.setCurrentIndex(0)

    def _on_submit(self):
        """Show ConfirmDialog, then reset the entire app"""
        data = self.review_page.current_data

        # Create a ConfirmDialog passing in the name and room, then show
        dlg = ConfirmDialog(data["name"], data["room"], self)
        dlg.exec()

        # Clear booking page data
        self.booking_page.clear_form()

        # Show the booking page
        self.stack.setCurrentIndex(0)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()