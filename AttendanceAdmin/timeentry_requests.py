from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QMenu, QToolButton
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import EmployeeAdmin.emp_admin_db as db
import os


class TimeEntryRequestTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 30, 30, 20)
        self.layout.setSpacing(20)

        title = QLabel("Time Entry Requests")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignLeft)

        self.request_table = QTableWidget()
        self.request_table.setColumnCount(8)
        self.request_table.setHorizontalHeaderLabels([
            "Employee ID", "Name", "Date", "Time In", "Time Out", "Reason", "Status", "Actions"
        ])
        self.request_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.layout.addWidget(title)
        self.layout.addWidget(self.request_table)

        print("[INIT] Loading time entry requests...")
        self.load_requests()
        
    def format_timedelta(self, td):
        if not td:
            return ""
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes = remainder // 60
        return f"{hours:02}:{minutes:02}"

    def load_requests(self):
        self.request_table.setRowCount(0)
        try:
            requests = db.get_pending_requests_with_name()
            print(f"[LOAD] Loaded {len(requests)} request(s).")
        except Exception as e:
            print("[DB ERROR] Cannot load time entry requests:", e)
            return

        for row, r in enumerate(requests):
            print(f"[ROW {row}] Data: {r}")
            (employee_id, first_name, last_name, date, time_in, time_out, reason, status, request_id) = r
            full_name = f"{first_name} {last_name}"

            self.request_table.insertRow(row)
            self.request_table.setItem(row, 0, QTableWidgetItem(employee_id))
            self.request_table.setItem(row, 1, QTableWidgetItem(full_name))
            self.request_table.setItem(row, 2, QTableWidgetItem(str(date)))
            formatted_time_in = self.format_timedelta(time_in)
            self.request_table.setItem(row, 3, QTableWidgetItem(formatted_time_in))

            self.request_table.setItem(row, 4, QTableWidgetItem(str(time_out)))
            self.request_table.setItem(row, 5, QTableWidgetItem(reason or ""))
            self.request_table.setItem(row, 6, QTableWidgetItem(status))

            action_button = QToolButton()
            action_button.setText("⋮")
            action_button.setFixedSize(30, 30)
            action_button.setStyleSheet("QToolButton { font-size: 18px; padding: 0px; }")

            menu = QMenu()
            menu.addAction("✅ Approve", lambda eid=employee_id, rid=request_id: self.handle_approve(eid, rid))
            menu.addAction("❌ Reject", lambda eid=employee_id, rid=request_id: self.handle_reject(eid, rid))

            action_button.menu = menu

            def show_menu():
                print(f"[ACTION] Showing action menu for employee {employee_id}, request {request_id}")
                menu.exec(action_button.mapToGlobal(action_button.rect().bottomLeft()))

            action_button.clicked.connect(show_menu)

            self.request_table.setCellWidget(row, 7, action_button)


    def handle_approve(self, employee_id, request_id):
        print(f"[APPROVE] Clicked for Employee ID: {employee_id}, Request ID: {request_id}")
        try:
            db.approve_request(str(request_id))
            print(f"[DB] Approved request ID: {request_id}")
        except Exception as e:
            print(f"[DB ERROR] Failed to approve request: {e}")
        self.load_requests()

    def handle_reject(self, employee_id, request_id):
        print(f"[REJECT] Clicked for Employee ID: {employee_id}, Request ID: {request_id}")
        try:
            db.reject_request(str(request_id))
            print(f"[DB] Rejected request ID: {request_id}")
        except Exception as e:
            print(f"[DB ERROR] Failed to reject request: {e}")
        self.load_requests()
