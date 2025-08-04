# The `DashboardPage` class creates a dashboard interface with clickable cards displaying information
# about employees and handles refreshing the counts dynamically.
from PySide6.QtWidgets import QWidget, QGridLayout, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt
import os
import EmployeeAdmin.emp_admin_db as db


class ClickableCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicked_callback = None
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        print("Card clicked!")
        if self.clicked_callback:
            self.clicked_callback()
        super().mousePressEvent(event)

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("DashboardPage")
        self.count_labels = {}
        self.load_stylesheet()
        self.init_ui()

    def load_stylesheet(self):
        try:
            qss_path = os.path.join(os.path.dirname(__file__), "..", "styles", "dashboard.qss")
            with open(os.path.abspath(qss_path), "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: styles/dashboard.qss not found.")

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(50, 30, 50, 30)

        container = QFrame()
        container.setObjectName("DashboardContainer")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 300, 700)
        container_layout.setSpacing(15)

        # Shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 160))
        container.setGraphicsEffect(shadow)

        grid = QGridLayout()
        grid.setSpacing(280)

        import EmployeeAdmin.emp_admin_db as db

        total_employees = db.get_total_employees()  
        inactive_count = db.count_inactive_employees()
        active_count = total_employees - inactive_count
        actve_employees = 5
        pending_leaves = 5
        online_employees = 5

        grid.addWidget(self.create_card(
            "Employees", active_count, "icons/employees.png", self.on_total_employees_clicked
        ), 0, 0)
        grid.addWidget(self.create_card("Active Employees", active_count, "icons/active.png"), 0, 1)
        grid.addWidget(self.create_card("Leave Requests", pending_leaves, "icons/leave.png"), 0, 2)
        grid.addWidget(self.create_card("Online Now", online_employees, "icons/monitor.png"), 1, 0)

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
            
        # Format count label: singular/plural
        if count == 1:
            count_text = "1"
        else:
            count_text = f"{count}"

        count_label = QLabel(count_text)
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

    def on_total_employees_clicked(self):
        parent = self.parentWidget()
        while parent and not hasattr(parent, 'switch_page'):
            parent = parent.parentWidget()
        if parent:
            parent.switch_page(1)
            if hasattr(parent, 'employees_page') and hasattr(parent.employees_page, 'load_employee_data'):
                parent.employees_page.load_employee_data()

    def refresh_counts(self):
        print("Refreshing counts...")
        import EmployeeAdmin.emp_admin_db as db
        total_employees = db.get_total_employees()
        inactive_employees = db.count_inactive_employees()
        active_employees = total_employees - inactive_employees

        self.count_labels["Employees"].setText(str(active_employees))


