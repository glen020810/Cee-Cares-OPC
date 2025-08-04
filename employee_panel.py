from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedLayout, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
import sys
from DashboardEmp.dashboard_emp import DashboardPage  # adjust path as needed
import EmployeeAdmin.emp_admin_db as db  # adjust path as needed
from PersonalInfoEmp.personal_info_emp import PersonalInfoPage
from AttendanceEmp.attendance_emp import AttendancePage
from LeaveEmp.leave_requests_emp import LeavePage
from PayslipEmp.payslip_emp import PayslipPage
from SettingsEmp.settings_emp import SettingsPage

class EmployeePanel(QMainWindow):
    def __init__(self, employee_id, employee_name):
        super().__init__()
        self.setWindowTitle("Employee Panel")
        self.setFixedSize(1100, 700)

        self.employee_id = employee_id
        self.employee_name = employee_name

        # ✅ Fetch first name from DB, fallback kung walang record
        try:
            self.first_name = db.get_first_name(self.employee_id)
            if not self.first_name:
                self.first_name = self.employee_name
        except:
            self.first_name = self.employee_name

        self.sidebar_expanded = True
        self.load_stylesheet()

        main_widget = QWidget()
        self.main_layout = QHBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QVBoxLayout()
        self.sidebar.setSpacing(15)
        self.sidebar.setContentsMargins(5, 5, 5, 5)

        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        self.toggle_btn.setFixedSize(30, 30)

        self.logo_label = QLabel()
        pixmap = QPixmap("Ceecaresopc.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)

        self.dashboard_btn = QPushButton("  Dashboard")
        self.dashboard_btn.setIcon(QIcon("icons/dashboard.png"))
        self.dashboard_btn.clicked.connect(lambda: self.switch_page(0))

        self.personal_info_btn = QPushButton("  Personal Info")
        self.personal_info_btn.setIcon(QIcon("icons/info.png"))
        self.personal_info_btn.clicked.connect(lambda: self.switch_page(1))

        self.attendance_btn = QPushButton("  Attendance")
        self.attendance_btn.setIcon(QIcon("icons/attendance.png"))
        self.attendance_btn.clicked.connect(lambda: self.switch_page(2))

        self.leave_btn = QPushButton("  Leave Application")
        self.leave_btn.setIcon(QIcon("icons/leave.png"))
        self.leave_btn.clicked.connect(lambda: self.switch_page(3))

        self.payslip_btn = QPushButton("  Payslip")
        self.payslip_btn.setIcon(QIcon("icons/payslip.png"))
        self.payslip_btn.clicked.connect(lambda: self.switch_page(4))

        self.sidebar.addWidget(self.toggle_btn)
        self.sidebar.addWidget(self.logo_label)
        self.sidebar.addSpacing(10)
        self.sidebar.addWidget(self.dashboard_btn)
        self.sidebar.addWidget(self.personal_info_btn)
        self.sidebar.addWidget(self.attendance_btn)
        self.sidebar.addWidget(self.leave_btn)
        self.sidebar.addWidget(self.payslip_btn)
        self.sidebar.addStretch()
        
        # ✅ Settings Button
        self.settings_btn = QPushButton("  Settings")
        self.settings_btn.setIcon(QIcon("icons/settings.png"))
        self.settings_btn.clicked.connect(self.open_settings)
        self.sidebar.addWidget(self.settings_btn)

        # ✅ Logout Button
        self.logout_btn = QPushButton("  Logout")
        self.logout_btn.setIcon(QIcon("icons/logout.png"))
        self.logout_btn.clicked.connect(self.logout)
        self.sidebar.addWidget(self.logout_btn)

        self.user_label = QLabel(f"  Employee: {self.first_name}")
        self.sidebar.addWidget(self.user_label)

        self.sidebar_frame = QFrame()
        self.sidebar_frame.setLayout(self.sidebar)
        self.sidebar_frame.setFixedWidth(180)
        self.sidebar_frame.setObjectName("Sidebar")

        # Pages
        self.stack = QStackedLayout()
        self.dashboard_page = DashboardPage(first_name=self.first_name)
        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(PersonalInfoPage(employee_id=self.employee_id))
        self.stack.addWidget(AttendancePage(employee_id=self.employee_id))
        self.stack.addWidget(LeavePage(employee_id=self.employee_id))
        self.stack.addWidget(PayslipPage(employee_id=self.employee_id))
        self.stack.addWidget(SettingsPage())

        content_widget = QWidget()
        content_widget.setLayout(self.stack)
        content_widget.setObjectName("ContentArea")

        # Combine Layouts
        self.main_layout.addWidget(self.sidebar_frame)
        self.main_layout.addWidget(content_widget)

        self.setCentralWidget(main_widget)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.sidebar_frame.setFixedWidth(50)
            self.logo_label.hide()
            self.dashboard_btn.setText("")
            self.personal_info_btn.setText("")
            self.attendance_btn.setText("")
            self.leave_btn.setText("")
            self.payslip_btn.setText("")
            self.settings_btn.setText("")
            self.logout_btn.setText("")
            self.user_label.hide()
        else:
            self.sidebar_frame.setFixedWidth(180)
            self.logo_label.show()
            self.dashboard_btn.setText("  Dashboard")
            self.personal_info_btn.setText("  Personal Info")
            self.attendance_btn.setText("  Attendance")
            self.leave_btn.setText("  Leave Application")
            self.payslip_btn.setText("  Payslip")
            self.settings_btn.setText("  Settings")
            self.logout_btn.setText("  Logout")
            self.user_label.show()

        self.sidebar_expanded = not self.sidebar_expanded

    def open_settings(self):
        print("Settings clicked")
        self.switch_page(5)
        # Pwede ka maglagay dito ng settings page kung gusto mo
        # Halimbawa: self.stack.addWidget(SettingsPage())
        # Tapos: self.switch_page(index_of_settings_page)
    
    def logout(self):
        self.close()
        from login import LoginWindow  # para di mag-loop import
        self.login_window = LoginWindow()
        self.login_window.show()

    def load_stylesheet(self):
        try:
            with open("styles/employee_panel.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: styles/employee_panel.qss not found. Default style applied.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Sample values for testing
    window = EmployeePanel(employee_id="EMP0001", employee_name="Juan Dela Cruz")
    window.show()
    sys.exit(app.exec())
