from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedLayout, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon, QFont
import sys, os
from EmployeeAdmin.employee_admin import EmployeePage
from DashboardAdmin.dashboard_admin import DashboardPage
from PayrollAdmin.payroll_admin import PayrollPage
from AttendanceAdmin.attendance_admin import AttendancePage
from LeaveAdmin.leave_requests_admin import LeaveRequestsAdmin

import EmployeeAdmin.emp_admin_db as db

class AdminPanel(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Admin Panel - Dashboard")
        self.setFixedSize(1100, 700)

        self.sidebar_expanded = True

        self.load_stylesheet()

        main_widget = QWidget()
        self.main_layout = QHBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Main sidebar layout
        self.sidebar = QVBoxLayout()
        self.sidebar.setContentsMargins(5, 5, 5, 5)
        self.sidebar.setSpacing(0)

        # Top part ng sidebar
        self.sidebar_top = QVBoxLayout()
        self.sidebar_top.setSpacing(15)

        # Bottom part ng sidebar
        self.sidebar_bottom = QVBoxLayout()
        self.sidebar_bottom.setSpacing(15)

        # Toggle button & logo
        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        self.toggle_btn.setFixedSize(30, 30)

        self.logo_label = QLabel()
        pixmap = QPixmap("Ceecaresopc.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        
        self.user_label = QLabel(username)
        self.user_label.setAlignment(Qt.AlignCenter)
        self.user_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.sidebar_top.addWidget(self.user_label)


        # Sidebar buttons
        self.dashboard_btn = QPushButton("  Dashboard")
        self.dashboard_btn.setIcon(QIcon("icons/dashboard.png"))
        self.dashboard_btn.clicked.connect(lambda: self.switch_page(0))

        self.employees_btn = QPushButton("  Employees")
        self.employees_btn.setIcon(QIcon("icons/employees.png"))
        self.employees_btn.clicked.connect(lambda: self.switch_page(1))

        self.payroll_btn = QPushButton("  Payroll")
        self.payroll_btn.setIcon(QIcon("icons/payroll.png"))
        self.payroll_btn.clicked.connect(self.toggle_payroll_submenu)

        # Payroll submenu setup (unchanged)
        self.payroll_submenu_widget = QWidget()
        self.payroll_submenu = QVBoxLayout()
        self.payroll_submenu.setContentsMargins(30, 0, 0, 0)

        self.salary_btn = QPushButton("Salary Management")
        self.salary_btn.clicked.connect(lambda: self.switch_page(2))

        self.leave_btn = QPushButton("Leave Management")
        self.leave_btn.clicked.connect(lambda: self.switch_page(3))

        self.payroll_submenu.addWidget(self.salary_btn)
        self.payroll_submenu.addWidget(self.leave_btn)
        self.payroll_submenu_widget.setLayout(self.payroll_submenu)
        self.payroll_submenu_widget.setVisible(False)
        
        self.attendance_btn = QPushButton("  Attendance Tracker")
        self.attendance_btn.setIcon(QIcon("icons/attendance.png"))  # Make sure you have this icon
        self.attendance_btn.clicked.connect(lambda: self.switch_page(4))


        self.monitoring_btn = QPushButton("  Screen Monitoring")
        self.monitoring_btn.setIcon(QIcon("icons/monitor.png"))
        self.monitoring_btn.clicked.connect(lambda: self.switch_page(5))

        self.settings_btn = QPushButton("  Settings")
        self.settings_btn.setIcon(QIcon("icons/settings.png"))
        self.settings_btn.clicked.connect(lambda: self.switch_page(6))

        # Add buttons to top layout
        self.sidebar_top.addWidget(self.toggle_btn)
        self.sidebar_top.addWidget(self.logo_label)
        self.sidebar_top.addSpacing(10)
        self.sidebar_top.addWidget(self.dashboard_btn)
        self.sidebar_top.addWidget(self.employees_btn)
        self.sidebar_top.addWidget(self.payroll_btn)
        self.sidebar_top.addWidget(self.payroll_submenu_widget)
        self.sidebar_top.addWidget(self.attendance_btn)
        self.sidebar_top.addWidget(self.monitoring_btn)
        self.sidebar_top.addWidget(self.settings_btn)
        self.sidebar_top.addStretch()

        # Bottom layout - Logout button
        self.logout_btn = QPushButton("  Logout")
        self.logout_btn.setIcon(QIcon("icons/logout.png"))
        self.logout_btn.clicked.connect(self.logout_action)
        self.sidebar_bottom.addWidget(self.logout_btn)

        # Combine top & bottom into main sidebar layout
        self.sidebar.addLayout(self.sidebar_top)
        self.sidebar.addLayout(self.sidebar_bottom)

        self.sidebar_frame = QFrame()
        self.sidebar_frame.setLayout(self.sidebar)
        self.sidebar_frame.setFixedWidth(180)
        self.sidebar_frame.setObjectName("Sidebar")

        # Content Area with Pages
        self.stack = QStackedLayout()
        
        dashboard_page = DashboardPage()
        dashboard_page.setParent(self)  # Allow access to switch_page()
        self.stack.addWidget(dashboard_page)


        self.employees_page = EmployeePage()
        self.stack.addWidget(self.employees_page)

        self.payroll_page = PayrollPage()
        self.stack.addWidget(self.payroll_page)
        
        self.leave_page = LeaveRequestsAdmin()
        self.stack.addWidget(self.leave_page)
        
        attendance_page = AttendancePage()
        self.stack.addWidget(attendance_page)

        monitoring_page = QLabel("Screen Monitoring Page")
        monitoring_page.setAlignment(Qt.AlignCenter)
        self.stack.addWidget(monitoring_page)
        
        from SettingsAdmin.settings_admin import SettingsPage
        settings_page = SettingsPage()
        self.stack.addWidget(settings_page)


        content_widget = QWidget()
        content_widget.setLayout(self.stack)
        content_widget.setObjectName("ContentArea")

        # Combine Layouts
        self.main_layout.addWidget(self.sidebar_frame)
        self.main_layout.addWidget(content_widget)

        self.setCentralWidget(main_widget)

    def switch_page(self, index):
        print(f"Switching to page {index}")
        self.stack.setCurrentIndex(index)

        if index == 0:
            dashboard_page = self.stack.widget(0)
            if hasattr(dashboard_page, 'refresh_counts'):
                print("Calling refresh_counts()")
                dashboard_page.refresh_counts()

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.sidebar_frame.setFixedWidth(50)
            self.logo_label.hide()
            self.dashboard_btn.setText("")
            self.employees_btn.setText("")
            self.payroll_btn.setText("")
            self.monitoring_btn.setText("")
            self.user_label.hide()
        else:
            self.sidebar_frame.setFixedWidth(180)
            self.logo_label.show()
            self.dashboard_btn.setText("  Dashboard")
            self.employees_btn.setText("  Employees")
            self.payroll_btn.setText("  Payroll")
            self.monitoring_btn.setText("  Screen Monitoring")
            self.user_label.show()

        self.sidebar_expanded = not self.sidebar_expanded

    def load_stylesheet(self):
        try:
            with open("styles/admin.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: styles/admin.qss not found. Default style applied.")

    def toggle_payroll_submenu(self):
        visible = self.payroll_submenu_widget.isVisible()
        self.payroll_submenu_widget.setVisible(not visible)
    
        if visible:
            self.payroll_btn.setText("  Payroll ▼")
        else:
            self.payroll_btn.setText("  Payroll ▲")
            
    def logout_action(self):
        print("Logging out...")
        from login import LoginWindow  # Safe na ilagay dito to avoid circular import issues
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminPanel("AdminUser")
    window.show()
    sys.exit(app.exec())
    