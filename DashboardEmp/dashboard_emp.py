from PySide6.QtWidgets import QWidget, QGridLayout, QFrame, QLabel, QVBoxLayout, QGraphicsDropShadowEffect, QHBoxLayout
from PySide6.QtGui import QPixmap, QColor, QFont
from PySide6.QtCore import Qt
import os
import EmployeeAdmin.emp_admin_db as db  # Change to your actual employee DB module

class ClickableCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicked_callback = None
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if self.clicked_callback:
            self.clicked_callback()
        super().mousePressEvent(event)

class DashboardPage(QWidget):
    def __init__(self, first_name="Employee"):
        super().__init__()
        self.first_name = first_name
        print("Welcome name passed:", self.first_name)

        self.setObjectName("DashboardPage")
        self.count_labels = {}
        self.load_stylesheet()
        self.init_ui()


    def load_stylesheet(self):
        try:
            qss_path = os.path.join(os.path.dirname(__file__), "..", "styles", "dashboard_emp.qss")
            print("Loading stylesheet from:", os.path.abspath(qss_path))
            with open(os.path.abspath(qss_path), "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: styles/dashboard_emp.qss not found.")

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(50, 30, 50, 320)  # ✅ Fix spacing

        container = QFrame()
        container.setObjectName("DashboardContainer")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(30, 30, 30, 150)  # ✅ Fix spacing
        container_layout.setSpacing(20)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 160))
        container.setGraphicsEffect(shadow)

        grid = QGridLayout()
        grid.setSpacing(20)  # ✅ Fix spacing

        # ✅ TEMP data or fallback if DB fails
        try:
            my_pending_leaves = db.get_my_pending_leaves() or 0
            my_approved_leaves = db.get_my_approved_leaves() or 0
            my_total_logins = db.get_my_login_days() or 0
            my_online_status = db.check_if_online() or False
        except Exception as e:
            print("DB error:", e)
            my_pending_leaves = 2
            my_approved_leaves = 5
            my_total_logins = 10
            my_online_status = True
            
        welcome_layout = QHBoxLayout()
        welcome_layout.setSpacing(20)

        welcome_label = QLabel("Welcome,")
        welcome_label.setObjectName("WelcomeLabel")

        name_label = QLabel(self.first_name)
        name_label.setObjectName("NameLabel")

        welcome_layout.addWidget(welcome_label)
        welcome_layout.addWidget(name_label)
        welcome_layout.addStretch() 

        container_layout.addLayout(welcome_layout)


        # Cards
        grid.addWidget(self.create_card("My Leave Requests", my_pending_leaves, "icons/leave.png"), 0, 0)
        grid.addWidget(self.create_card("Approved Leaves", my_approved_leaves, "icons/approved.png"), 0, 1)
        grid.addWidget(self.create_card("Days Logged In", my_total_logins, "icons/calendar.png"), 1, 0)
        grid.addWidget(self.create_card("Online Status", 1 if my_online_status else 0, "icons/monitor.png"), 1, 1)

        container_layout.addLayout(grid)
        main_layout.addWidget(container)

    def create_card(self, title, count, icon_path, on_click=None):
        card = ClickableCard(self)
        card.setFixedSize(220, 120)
        card.setObjectName("DashboardCard")
        card.clicked_callback = on_click

        vbox = QVBoxLayout(card)
        vbox.setContentsMargins(20, 10, 10, 10)

        icon_label = QLabel()
        icon_label.setObjectName("CardIcon")
        icon_label.setStyleSheet("background: transparent; border: none;")
        icon_label.setFixedSize(100, 80)

        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            icon_label.setPixmap(pixmap.scaled(100, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            print(f"Warning: {icon_path} not found or failed to load.")
            icon_label.setText("❌")  # Fallback if icon missing

        count_label = QLabel(str(count))
        count_label.setStyleSheet("""
            background: transparent;
            border: none;
            color: white;
            font-size: 40px;
            font-weight: bold;
        """)
        count_label.setFixedSize(50, 35)
        count_label.setAttribute(Qt.WA_TranslucentBackground)
        count_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        title_label = QLabel(title)
        title_label.setStyleSheet("background: transparent; border: none;")
        title_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        vbox.addWidget(icon_label, alignment=Qt.AlignLeft)
        vbox.addWidget(count_label, alignment=Qt.AlignRight)
        vbox.addWidget(title_label, alignment=Qt.AlignRight)

        self.count_labels[title] = count_label

        return card

    def refresh_counts(self):
        # Optional: refresh logic if needed
        pass
