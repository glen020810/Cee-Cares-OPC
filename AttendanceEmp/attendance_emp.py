from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QFrame, QGraphicsDropShadowEffect,
    QListWidget, QListWidgetItem, QPushButton, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtGui import QColor, QFont, QPixmap, QIcon
from PySide6.QtCore import Qt, QDateTime
import os
import EmployeeAdmin.emp_admin_db as db
from datetime import datetime, timedelta
from AttendanceEmp.time_entry import TimeEntryTab  # Make sure this file exists


class AttendancePage(QWidget):
    def __init__(self, employee_id):
        super().__init__()
        self.employee_id = employee_id
        self.setObjectName("AttendancePage")
        self.load_stylesheet()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(50, 30, 50, 30)

        container = QFrame()
        container.setObjectName("ContainerFrame")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 160))
        container.setGraphicsEffect(shadow)

        tabs = QTabWidget()
        tabs.setObjectName("AttendanceTabs")

        # === TAB 1: Records ===
        records_tab = QWidget()
        records_layout = QVBoxLayout(records_tab)

        title = QLabel("Today")
        title.setAlignment(Qt.AlignLeft)
        title.setFont(QFont("Arial", 18, QFont.Bold))

        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(6)
        self.attendance_table.setHorizontalHeaderLabels(["Employee ID", "Date", "Name", "Status", "Time In", "Time Out"])
        self.attendance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.attendance_table.setObjectName("AttendanceTable")

        missing_label = QLabel("Missing Records")
        missing_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.missing_list = QListWidget()
        self.missing_list.setObjectName("MissingList")

        records_layout.addWidget(title)
        records_layout.addWidget(self.attendance_table)
        records_layout.addWidget(missing_label)
        records_layout.addWidget(self.missing_list)

        self.load_attendance_records()
        
        tabs.addTab(records_tab, "Attendance")
        
        # === TAB 2: Time Entry (Calendar View with Grid) ===
        time_entry_tab = TimeEntryTab(self.employee_id)
        tabs.addTab(time_entry_tab, "Time Entry")

        # === TAB 3: Manual Entry ===
        manual_tab = QWidget()
        manual_layout = QVBoxLayout(manual_tab)

        button_layout = QHBoxLayout()
        self.time_in_btn = QPushButton("Time In")
        self.time_out_btn = QPushButton("Time Out")
        self.time_in_btn.clicked.connect(self.time_in)
        self.time_out_btn.clicked.connect(self.time_out)
        button_layout.addWidget(self.time_in_btn)
        button_layout.addWidget(self.time_out_btn)

        entry_form_layout = QHBoxLayout()
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD")
        self.time_in_input = QLineEdit()
        self.time_in_input.setPlaceholderText("Time In (HH:MM)")
        self.time_out_input = QLineEdit()
        self.time_out_input.setPlaceholderText("Time Out (HH:MM)")
        add_manual_btn = QPushButton("Add Manual Entry")
        add_manual_btn.clicked.connect(self.add_manual_entry)

        entry_form_layout.addWidget(self.date_input)
        entry_form_layout.addWidget(self.time_in_input)
        entry_form_layout.addWidget(self.time_out_input)
        entry_form_layout.addWidget(add_manual_btn)

        manual_layout.addLayout(button_layout)
        manual_layout.addLayout(entry_form_layout)

        tabs.addTab(manual_tab, "Manual Entry")
        
        # === TAB 4: History ===
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)

        history_label = QLabel("Attendance Records")
        history_label.setAlignment(Qt.AlignLeft)
        history_label.setFont(QFont("Arial", 16, QFont.Bold))

        self.history_list = QListWidget()
        self.history_list.setObjectName("HistoryList")
        
        # Time Entry History Label and List
        time_entry_label = QLabel("Time Entry Records")
        time_entry_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.time_entry_list = QListWidget()
        self.time_entry_list.setObjectName("TimeEntryList")

        self.load_history_records()  # Tawagin ang method para i-load ang data

        history_layout.addWidget(history_label)
        history_layout.addWidget(self.history_list)
        history_layout.addWidget(time_entry_label)
        history_layout.addWidget(self.time_entry_list)

        tabs.addTab(history_tab, "History")


        # Add everything to container
        container_layout.addWidget(tabs)
        main_layout.addWidget(container)

    def load_attendance_records(self):
        print("🔄 Loading today's attendance record...")

        self.attendance_table.setRowCount(0)
        self.missing_list.clear()

        today = datetime.today().date()
        current_date_str = today.strftime('%Y-%m-%d')

        try:
            records = db.get_my_attendance_records(self.employee_id) or []
            employee = db.get_employee_by_id(self.employee_id)
        except:
            records = []
            employee = None

        full_name = f"{employee['first_name']} {employee['last_name']}" if employee else "Unknown"
        profile_path = employee['profile_image'] if employee and employee['profile_image'] else ""

        record_map = {rec[0]: rec for rec in records}
        rec = record_map.get(today)

        if rec:
            print(f"✅ Record found for today ({today}): {rec}")
            time_in = rec[1] if rec[1] else "N/A"
            time_out = rec[2] if rec[2] else "N/A"
            status = "On Time"

            try:
                if isinstance(time_in, timedelta):
                    total_seconds = int(time_in.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    if hours > 9 or (hours == 9 and minutes > 0):
                        status = "Late"
            except:
                status = "N/A"

            self.attendance_table.insertRow(0)
            self.attendance_table.setItem(0, 0, QTableWidgetItem(self.employee_id))
            self.attendance_table.setItem(0, 1, QTableWidgetItem(today.strftime('%Y-%m-%d')))

            name_item = QTableWidgetItem(full_name)
            if profile_path and os.path.exists(profile_path):
                pixmap = QPixmap(profile_path).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon = QIcon(pixmap)
                name_item.setIcon(icon)

            self.attendance_table.setItem(0, 2, name_item)
            self.attendance_table.setItem(0, 3, QTableWidgetItem(status))
            self.attendance_table.setItem(0, 4, QTableWidgetItem(str(time_in)))
            self.attendance_table.setItem(0, 5, QTableWidgetItem(str(time_out)))
        else:
            print("🚫 No attendance record for today.")
            item_text = f"{today} | Time In: No Entry | Time Out: No Entry"
            self.missing_list.addItem(QListWidgetItem(item_text))
            
        from datetime import date

        start_date = date(today.year, 7, 1)
        end_date = today - timedelta(days=1)
        days_range = (end_date - start_date).days + 1

        for i in range(days_range):
            day = start_date + timedelta(days=i)
            rec = record_map.get(day)

            if rec:
                time_in = rec[1]
                time_out = rec[2]
                if not time_in or not time_out:
                    item_text = f"{day} | Time In: {'No Entry' if not time_in else time_in} | Time Out: {'No Entry' if not time_out else time_out}"
                    self.missing_list.addItem(QListWidgetItem(item_text))
            else:
                item_text = f"{day} | Time In: No Entry | Time Out: No Entry"
                self.missing_list.addItem(QListWidgetItem(item_text))

    def time_in(self):
        current_date = QDateTime.currentDateTime().toString("yyyy-MM-dd")

        # ⛔ Check if already timed in
        existing = db.get_attendance_by_date(self.employee_id, current_date)
        if existing and existing[1]:  # May time_in na
            QMessageBox.warning(self, "Already Timed In", "You have already timed in today.")
            return

        current_time = QDateTime.currentDateTime().toString("HH:mm")
        success = db.time_in(self.employee_id, current_date, current_time)
        if success:
            QMessageBox.information(self, "Success", "Time In recorded.")
            self.load_attendance_records()
        else:
            QMessageBox.warning(self, "Error", "Failed to record Time In.")

    def time_out(self):
        current_date = QDateTime.currentDateTime().toString("yyyy-MM-dd")
        current_time = QDateTime.currentDateTime().toString("HH:mm")
        success = db.time_out(self.eemployee_idmp_id, current_date, current_time)
        if success:
            QMessageBox.information(self, "Success", "Time Out recorded.")
            self.load_attendance_records()
        else:
            QMessageBox.warning(self, "Error", "Failed to record Time Out.")

    def add_manual_entry(self):
        date = self.date_input.text()
        time_in = self.time_in_input.text()
        time_out = self.time_out_input.text()

        if not date or not time_in or not time_out:
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        success = db.add_manual_attendance(self.employee_id, date, time_in, time_out)
        if success:
            QMessageBox.information(self, "Success", "Manual attendance added.")
            self.load_attendance_records()
            self.date_input.clear()
            self.time_in_input.clear()
            self.time_out_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Failed to add manual attendance.")
            
    def load_history_records(self):
        print("📚 Loading history records (excluding today)...")
        self.history_list.clear()

        today = datetime.today().date()
        shown_entries = set()
        
        try:
            history = db.get_attendance_history(self.employee_id) or []
            for rec in history:
                date = rec[0]
                if isinstance(date, str):
                    date = datetime.strptime(date, "%Y-%m-%d").date()

                if date == today:
                    continue  # skip today's record

                time_in = rec[1] or "N/A"
                time_out = rec[2] or "N/A"
                key = (date, str(time_in))
                if key in shown_entries:
                    continue
                shown_entries.add(key)
                
                # 🕘 Determine Status
                if time_in == "N/A" or time_out == "N/A":
                    status = "N/A"
                else:
                    try:
                        time_str = str(time_in)
                        time_obj = datetime.strptime(time_str, "%H:%M:%S" if len(time_str.split(":")) == 3 else "%H:%M")
                        status = "Late" if time_obj.hour > 9 or (time_obj.hour == 9 and time_obj.minute > 0) else "On Time"
                    except Exception as e:
                        print(f"⚠️ Time parsing error for {time_in}: {e}")
                        status = "N/A"

                item_text = f"{date} | Time In: {time_in} | Time Out: {time_out} | Status: {status}"
                self.history_list.addItem(QListWidgetItem(item_text))

        except Exception as e:
            print(f"❌ Error loading history: {e}")

        # ✅ Time Entry Requests (from `attendance_requests` table)
        try:
            requests = db.get_approved_time_entries(self.employee_id) or []
            for rec in requests:
                date = rec[0]
                if isinstance(date, str):
                    date = datetime.strptime(date, "%Y-%m-%d").date()

                time_in = rec[1] or "N/A"
                time_out = rec[2] or "N/A"
                status = rec[3]

                entry_text = f"{date} | Time In: {time_in} | Time Out: {time_out} | Status: {status}"
                self.time_entry_list.addItem(QListWidgetItem(entry_text))

        except Exception as e:
            print(f"❌ Error loading time entry history: {e}")

    def load_stylesheet(self):
        try:
            qss_path = os.path.join(os.path.dirname(__file__), "..", "styles", "attendance_emp.qss")
            with open(os.path.abspath(qss_path), "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: styles/attendance_emp.qss not found. Default style applied.")
