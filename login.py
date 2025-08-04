from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QMessageBox, QApplication, QHBoxLayout, QStackedLayout, QFrame
)
from PySide6.QtGui import QIcon, QCursor, QAction
from PySide6.QtCore import Qt

# Assuming meron kang emp_admin_db.py na may check_credentials function
import EmployeeAdmin.emp_admin_db as emp_admin_db
from employee_panel import EmployeePanel
from admin_panel import AdminPanel
import sys
from database import validate_user
from change_password import ChangePasswordWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 380)

        self.load_stylesheet()

        self.role_selector = QComboBox()
        self.role_selector.addItems(["Admin", "Employee"])

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("EMPXXXX")
        self.username_input.returnPressed.connect(self.handle_login)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.handle_login)

        self.show_password_action = QAction(QIcon("icons/eye_closed.png"), "Show/Hide Password", self.password_input)
        self.show_password_action.setCheckable(True)
        self.show_password_action.triggered.connect(self.toggle_password_visibility)
        self.password_input.addAction(self.show_password_action, QLineEdit.TrailingPosition)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)

        self.forgot_password_label = QLabel('<a href="#">Forgot Password?</a>')
        self.forgot_password_label.setAlignment(Qt.AlignRight)
        self.forgot_password_label.setOpenExternalLinks(False)
        self.forgot_password_label.linkActivated.connect(self.handle_forgot_password)
        self.forgot_password_label.setCursor(QCursor(Qt.PointingHandCursor))

        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("Employee Management")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(self.role_selector)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.forgot_password_label)
        layout.addWidget(self.login_button)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_stylesheet(self):
        try:
            with open("styles/login.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: styles/login.qss not found. Default style applied.")

    def toggle_password_visibility(self, checked):
        if checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.show_password_action.setIcon(QIcon("icons/eye_open.png"))
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.show_password_action.setIcon(QIcon("icons/eye_closed.png"))

    def handle_login(self):
        role = self.role_selector.currentText()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        if role == "Employee":
            emp_id = username.replace("-", "").strip().upper()

            if not emp_id.startswith("EMP"):
                QMessageBox.warning(self, "Invalid", "Employee ID must start with EMP")
                return

            if emp_admin_db.check_employee_credentials(emp_id, password):
                if password == "1234":
                    QMessageBox.information(self, "Change Password", "First login detected. Please change your password.")
                    self.change_password_window = ChangePasswordWindow(emp_id)
                    self.change_password_window.show()
                else:
                    self.open_employee_panel(emp_id)
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid credentials.")


        elif role == "Admin":
            role_from_db = validate_user(username, password)
            if role_from_db == "admin":
                self.open_admin_panel(username)
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid credentials.")

    def open_employee_panel(self, emp_id):
        employee_data = emp_admin_db.get_employee_by_id(emp_id)
        if employee_data:
            employee_name = employee_data['first_name']
        else:
            employee_name = "Employee"  # Fallback, pero ideally di dapat mangyari kung validated na
        self.employee_panel = EmployeePanel(emp_id, employee_name)
        self.employee_panel.show()
        self.close()

    def open_admin_panel(self, username):
        self.admin_panel = AdminPanel(username)
        self.admin_panel.show()
        self.close()

    def handle_forgot_password(self):
        QMessageBox.information(self, "Forgot Password", "Please contact the administrator to reset your password.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
