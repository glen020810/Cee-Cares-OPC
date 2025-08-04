from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
import EmployeeAdmin.emp_admin_db as db  # Adjust if needed

class ServerSettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Recent Employee Logins:")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.requests_list = QListWidget()

        self.refresh_btn = QPushButton("Refresh Logs")
        self.refresh_btn.clicked.connect(self.load_login_logs)
        self.refresh_btn.setStyleSheet("background-color: #3498db; color: white; padding: 5px;")

        layout.addWidget(title)
        layout.addWidget(self.requests_list)
        layout.addWidget(self.refresh_btn)

        self.load_login_logs()

    def load_login_logs(self):
        """Load recent login records from the database."""
        self.requests_list.clear()
        try:
            logs = db.get_login_logs(limit=50)

            if not logs:
                self.requests_list.addItem("No recent logins found.")
                return

            for log in logs:
                item_text = (
                    f"Employee: {log['employee_id']}  |  "
                    f"IP: {log['ip_address']}  |  "
                    f"PC: {log['hostname']}  |  "
                    f"{log['login_time']}"
                )
                list_item = QListWidgetItem(item_text)
                self.requests_list.addItem(list_item)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load login logs: {e}")
