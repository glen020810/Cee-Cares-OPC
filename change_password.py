from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import EmployeeAdmin.emp_admin_db as db

class ChangePasswordWindow(QWidget):
    def __init__(self, employee_id):
        super().__init__()
        self.employee_id = employee_id
        self.setWindowTitle("Change Password")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Enter new password")
        self.new_password_input.setEchoMode(QLineEdit.Password)

        self.confirm_btn = QPushButton("Confirm")
        self.confirm_btn.clicked.connect(self.change_password)

        layout.addWidget(QLabel("Please change your password:"))
        layout.addWidget(self.new_password_input)
        layout.addWidget(self.confirm_btn)

        self.setLayout(layout)

    def change_password(self):
        new_password = self.new_password_input.text().strip()

        if new_password and new_password != "1234":
            db.update_employee_password(self.employee_id, new_password)
            QMessageBox.information(self, "Success", "Password changed successfully. Please log in again.")
            self.close()
        else:
            QMessageBox.warning(self, "Invalid", "New password cannot be empty or '1234'.")
