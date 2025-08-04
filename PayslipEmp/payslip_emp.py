from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QGraphicsDropShadowEffect, QPushButton
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt
import os
import EmployeeAdmin.emp_admin_db as db  # Adjust path as needed

class PayslipPage(QWidget):
    def __init__(self, employee_id):
        super().__init__()
        self.employee_id = employee_id
        self.setObjectName("PayslipPage")
        self.load_stylesheet()
        self.init_ui()

    def load_stylesheet(self):
        try:
            qss_path = os.path.join(os.path.dirname(__file__), "..", "styles", "payslip_emp.qss")
            with open(os.path.abspath(qss_path), "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: styles/payslip_emp.qss not found. Default style applied.")

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(50, 30, 50, 30)

        container = QFrame()
        container.setObjectName("PayslipContainer")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(30, 30, 30, 30)
        container_layout.setSpacing(20)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 160))
        container.setGraphicsEffect(shadow)

        title_label = QLabel("Payslip Viewer")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))

        try:
            latest_payslip_date = db.get_latest_payslip_date(self.employee_id) or "N/A"
        except:
            latest_payslip_date = "N/A"

        latest_label = QLabel(f"Latest Payslip Date: {latest_payslip_date}")
        latest_label.setAlignment(Qt.AlignCenter)
        latest_label.setFont(QFont("Arial", 14))

        view_button = QPushButton("View Payslips")
        view_button.clicked.connect(self.view_payslips)

        container_layout.addWidget(title_label)
        container_layout.addWidget(latest_label)
        container_layout.addWidget(view_button)

        layout.addWidget(container)

    def view_payslips(self):
        print(f"{self.employee_id} clicked View Payslips")
