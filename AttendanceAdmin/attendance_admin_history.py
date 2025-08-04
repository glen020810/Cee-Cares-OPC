from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PySide6.QtGui import QFont, QColor, QBrush
from PySide6.QtCore import Qt
from datetime import timedelta, date as dt_date
from EmployeeAdmin.emp_admin_db import get_all_attendance_records, get_history_requests_with_name


class HistoryTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 30, 10, 30)
        layout.setSpacing(30)

        # 📌 Section 1: Attendance History
        attendance_label = QLabel("Employee Attendance History")
        attendance_label.setFont(QFont("Arial", 13, QFont.Bold))
        layout.addWidget(attendance_label)

        self.attendance_list = QListWidget()
        layout.addWidget(self.attendance_list)

        # 📌 Section 2: Time Entry Request History
        request_label = QLabel("Time Entry Request History")
        request_label.setFont(QFont("Arial", 13, QFont.Bold))
        layout.addWidget(request_label)

        self.request_list = QListWidget()
        layout.addWidget(self.request_list)

        # Load data
        self.load_attendance_data()
        self.load_request_data()

    def format_time(self, t):
        if isinstance(t, timedelta):
            total_seconds = int(t.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours:02}:{minutes:02}"
        return str(t) if t else "N/A"

    def load_attendance_data(self):
        today = dt_date.today()
        try:
            records = get_all_attendance_records()
            old_records = [r for r in records if r[1] < today]

            for record in old_records:
                employee_id, date, fname, lname, _, time_in, time_out = record
                full_name = f"{fname} {lname}"
                time_in_str = self.format_time(time_in)
                time_out_str = self.format_time(time_out)

                # Determine Status
                if isinstance(time_in, timedelta) and time_in.total_seconds() > 9 * 60 * 60:
                    status = "Late"
                else:
                    status = "On Time"

                entry = (
                    f"Employee ID: {employee_id} | Name: {full_name} | Date: {date} | "
                    f"Time In: {time_in_str} | Time Out: {time_out_str} | Status: {status}"
                )
                self.attendance_list.addItem(QListWidgetItem(entry))

        except Exception as e:
            print(f"❌ Error loading attendance data: {e}")

    def load_request_data(self):
        try:
            records = get_history_requests_with_name()
            for record in records:
                employee_id, fname, lname, date, time_in, time_out, _, status, _ = record
                full_name = f"{fname} {lname}"
                time_in_str = self.format_time(time_in)
                time_out_str = self.format_time(time_out)

                entry = (
                    f"Employee ID: {employee_id} | Name: {full_name} | Date: {date} | "
                    f"Time In: {time_in_str} | Time Out: {time_out_str} | Status: {status}"
                )
                self.request_list.addItem(QListWidgetItem(entry))

        except Exception as e:
            print(f"❌ Error loading request data: {e}")
            

