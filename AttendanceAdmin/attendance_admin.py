from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QLabel, QGraphicsDropShadowEffect, QTableWidget,
    QTableWidgetItem, QHeaderView, QTabWidget
)
from PySide6.QtGui import QColor, QFont, QPixmap, QIcon
from PySide6.QtCore import Qt
import os
import EmployeeAdmin.emp_admin_db as db  # Make sure this has get_all_attendance_records()
from datetime import timedelta
from datetime import date as dt_date
from AttendanceAdmin.timeentry_requests import TimeEntryRequestTab
from AttendanceAdmin.attendance_admin_history import HistoryTab



class AttendancePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("AttendancePage")
        self.load_stylesheet()

        self.tab_widget = QTabWidget()
        self.attendance_tab = QWidget()
        self.history_tab = HistoryTab()

        self.tab_widget.addTab(self.attendance_tab, "Attendance")
        
        self.time_entry_request_tab = TimeEntryRequestTab()
        self.tab_widget.addTab(self.time_entry_request_tab, "Time Entry Request")

        self.history_tab = HistoryTab()
        self.tab_widget.addTab(self.history_tab, "History")


        # 👇 This part replaces previous layout assignment
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(50, 30, 50, 30)

        container = QFrame()
        container.setObjectName("AttendanceContainer")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(30, 30, 30, 50)
        container_layout.setSpacing(20)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 160))
        container.setGraphicsEffect(shadow)

        container_layout.addWidget(self.tab_widget)  # ✅ Put tab widget inside the styled container
        outer_layout.addWidget(container)

        self.setLayout(outer_layout)

        self.init_attendance_tab_ui()


    def init_attendance_tab_ui(self):
        layout = QVBoxLayout(self.attendance_tab)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(20, 30, 20, 20)
        layout.setSpacing(20)

        title_label = QLabel("Employee Attendance")
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))

        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(6)
        self.attendance_table.setHorizontalHeaderLabels([
            "Employee ID", "Date", "Name", "Status", "Time In", "Time Out"
        ])
        self.attendance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.attendance_table.setObjectName("AdminAttendanceTable")

        layout.addWidget(title_label)
        layout.addWidget(self.attendance_table)

        self.load_all_attendance()



    def load_stylesheet(self):
        qss_path = os.path.join(os.path.dirname(__file__), "..", "styles", "attendance_admin.qss")
        try:
            with open(os.path.abspath(qss_path), "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: attendance_admin.qss not found. Using default style.")


    def format_time(self, t):
        if isinstance(t, timedelta):
            total_seconds = int(t.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours:02}:{minutes:02}"
        return "N/A"


    def load_all_attendance(self):
        self.attendance_table.setRowCount(0)
        today = dt_date.today()

        try:
            all_records = db.get_all_attendance_records()
            print(f"[DEBUG] Retrieved {len(all_records)} attendance records.")
        except Exception as e:
            print(f"[❌ ERROR] Failed to fetch records: {e}")
            return

        row = 0
        for record in all_records:
            employee_id, date, first_name, last_name, profile_img, time_in, time_out = record
            if date != today:
                continue

            full_name = f"{first_name} {last_name}"
            status = "On Time"
 
            # Determine if late
            try:
                if isinstance(time_in, timedelta) and time_in.total_seconds() / 60 > 540:
                    status = "Late"
            except Exception as e:
                status = "N/A"

            # Format times
            formatted_time_in = self.format_time(time_in)
            formatted_time_out = self.format_time(time_out)

            self.attendance_table.insertRow(row)
            self.attendance_table.setItem(row, 0, QTableWidgetItem(employee_id))
            self.attendance_table.setItem(row, 1, QTableWidgetItem(str(date)))

            name_item = QTableWidgetItem(full_name)

            # Handle image
            if profile_img:
                if not os.path.isabs(profile_img):
                    profile_img = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images", profile_img))
                if os.path.exists(profile_img):
                    pixmap = QPixmap(profile_img).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    name_item.setIcon(QIcon(pixmap))
                else:
                    print(f"[⚠️ MISSING] Profile image not found: {profile_img}")
            self.attendance_table.setItem(row, 2, name_item)
            self.attendance_table.setItem(row, 3, QTableWidgetItem(status))
            self.attendance_table.setItem(row, 4, QTableWidgetItem(formatted_time_in))
            self.attendance_table.setItem(row, 5, QTableWidgetItem(formatted_time_out or "N/A"))

            row += 1
