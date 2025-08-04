from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from EmployeeAdmin.emp_admin_db import get_all_leave_requests  # Make sure this returns history data

class LeaveHistoryTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 30, 10, 30)
        layout.setSpacing(30)

        # 📌 Section Title
        leave_label = QLabel("Employee Leave Request History")
        leave_label.setFont(QFont("Arial", 13, QFont.Bold))
        layout.addWidget(leave_label)

        self.leave_list = QListWidget()
        layout.addWidget(self.leave_list)

        self.load_leave_history()

    def load_leave_history(self):
        try:
            records = get_all_leave_requests()
            self.leave_list.clear()
            for record in records:
                (
                    request_id,
                    employee_id,
                    first_name,
                    last_name,
                    leave_type,
                    paid_status,
                    start_date,
                    end_date,
                    reason,
                    status,
                    reviewed_by,     # ✅ still unpacked, but not shown
                    reviewed_at
                ) = record

                employee_name = f"{employee_id} - {first_name} {last_name}"

                entry = (
                    f"Employee: {employee_name} | Type: {leave_type} | Payment: {paid_status} | "
                    f"Start: {start_date} | End: {end_date} | Reason: {reason} | Status: {status}"
                )
                self.leave_list.addItem(QListWidgetItem(entry))

        except Exception as e:
            print(f"❌ Error loading leave request history: {e}")

