from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QGraphicsDropShadowEffect,
    QLabel, QTableWidget, QHeaderView, QTableWidgetItem, QLineEdit, QComboBox, QTabWidget
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from PayrollAdmin.enroll_payroll import EnrollPayrollWindow
from PayrollAdmin.payroll_profiles_window import PayrollProfileListWindow
from EmployeeAdmin.emp_admin_db import get_enrolled_payroll_profiles # ✅ Make sure this is a callable function that returns a list of dicts
from datetime import date


class PayrollPage(QWidget):
    def __init__(self):
        super().__init__()
        self.load_stylesheet()
        self.setup_ui()
        self.load_enrolled_payrolls()  # ✅ Load data at startup

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setAlignment(Qt.AlignTop)

        container = QFrame()
        container.setObjectName("PayrollContainer")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(50, 50, 0, 30)
        container_layout.setSpacing(0)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 160))
        container.setGraphicsEffect(shadow)

        tab_widget = QTabWidget()
        tab_widget.setObjectName("PayrollTabs")

        # --- Tab 1: Enrolled Payrolls ---
        payroll_tab = QWidget()
        payroll_layout = QVBoxLayout(payroll_tab)
        payroll_layout.setContentsMargins(20, 20, 20, 20)
        payroll_layout.setSpacing(15)

        top_bar = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search Payroll")

        self.filter_box = QComboBox()
        self.filter_box.addItems(["All", "This Month", "Last Month"])

        self.add_btn = QPushButton("Enroll to Payroll")
        self.add_btn.setFixedSize(150, 30)
        self.add_btn.setObjectName("addPayrollBtn")
        self.add_btn.clicked.connect(self.open_enroll_window)

        top_bar.addWidget(self.search_box)
        top_bar.addWidget(self.filter_box)
        top_bar.addStretch()
        top_bar.addWidget(self.add_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Period", "Total Pay", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(50)

        payroll_layout.addLayout(top_bar)
        payroll_layout.addWidget(self.table)

        # --- Tab 2: Registered Employees ---
        registered_tab = PayrollProfileListWindow()

        tab_widget.addTab(payroll_tab, "Enrolled Payrolls")
        tab_widget.addTab(registered_tab, "Registered Employees")

        container_layout.addWidget(tab_widget)
        main_layout.addWidget(container)

    def open_enroll_window(self):
        self.enroll_window = EnrollPayrollWindow()
        self.enroll_window.finished.connect(self.load_enrolled_payrolls)  # ✅ Auto-refresh on close
        self.enroll_window.show()

    def load_enrolled_payrolls(self):
        today = date.today()
        testing_mode = True  # 🔧 Set to False kapag live/production na

        # Pag production mode na, limit to 14, 29, or 30 only
        if not testing_mode:
            if today.day not in (14, 29, 30):
                print("[INFO] Not a payroll approval day. Skipping data load.")
                return

        try:
            payrolls = get_enrolled_payroll_profiles()  # ✅ Must return list[dict]
        except Exception as e:
            print("[ERROR] Failed to load payrolls:", e)
            payrolls = []

        self.table.setRowCount(0)

        for row, payroll in enumerate(payrolls):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(payroll.get("employee_id", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(str(payroll.get("employee_name", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(payroll.get("period", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(f"₱{payroll.get('total_pay', 0):,.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(str(payroll.get("status", "Pending"))))

    def load_stylesheet(self):
        try:
            with open("styles/payroll.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: styles/payroll.qss not found.")
