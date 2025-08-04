# EmployeeAdmin/AttendanceEmp/time_entry.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QDateEdit, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QDialog, QDialogButtonBox, QTimeEdit
)
from PySide6.QtCore import QDate
from PySide6.QtGui import QColor
from datetime import datetime, timedelta

import EmployeeAdmin.emp_admin_db as db  # adjust if needed

class TimeEntryTab(QWidget):
    def __init__(self, employee_id):
        super().__init__()
        self.employee_id = employee_id
        
        self.init_ui()
        # Inside TimeEntryTab.__init__
        self.setObjectName("TimeEntryTab")
        self.table.setObjectName("TimeGridTable")
        self.from_date.setObjectName("FromDateEdit")
        self.to_date.setObjectName("ToDateEdit")
        self.load_btn.setObjectName("LoadButton")
        self.table.cellDoubleClicked.connect(self.open_time_edit_dialog)

        
        self.load_stylesheet()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Date range picker
        date_range_layout = QHBoxLayout()
        self.from_date = QDateEdit(QDate.currentDate().addDays(-6))
        self.to_date = QDateEdit(QDate.currentDate())
        self.from_date.setCalendarPopup(True)
        self.to_date.setCalendarPopup(True)

        self.load_btn = QPushButton("Load")
        self.load_btn.clicked.connect(self.load_time_grid)

        date_range_layout.addWidget(QLabel("From:"))
        date_range_layout.addWidget(self.from_date)
        date_range_layout.addWidget(QLabel("To:"))
        date_range_layout.addWidget(self.to_date)
        date_range_layout.addWidget(self.load_btn)

        layout.addLayout(date_range_layout)

        # Time grid table
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked)
        layout.addWidget(self.table)
    
    def load_time_grid(self):
        from_date = self.from_date.date().toPython()
        to_date = self.to_date.date().toPython()
        num_days = (to_date - from_date).days + 1

        print(f"[DEBUG] From: {from_date}, To: {to_date}, Days: {num_days}")

        if num_days > 7:
            QMessageBox.warning(self, "Limit", "Maximum 7 days only.")
            return

        self.table.clear()
        self.table.setColumnCount(num_days)
        self.table.setRowCount(12)
        self.table.setHorizontalHeaderLabels([
            (from_date + timedelta(days=i)).strftime("%a\n%Y-%m-%d") for i in range(num_days)
        ])
        self.table.setVerticalHeaderLabels([
            (datetime(2000, 1, 1, 7 + i)).strftime("%I:%M %p") for i in range(12)
        ])

        # Get attendance records from DB
        records = db.get_attendance_range(
            self.employee_id, from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d')
        )
        print(f"\n[DEBUG] Raw DB Records: {records}")

        record_map = {
            r[0].strftime('%Y-%m-%d'): {"time_in": r[1], "time_out": r[2]}
            for r in records
        }
        print(f"[DEBUG] Mapped Records: {record_map}")

        for col, day_offset in enumerate(range(num_days)):
            date_str = (from_date + timedelta(days=day_offset)).strftime('%Y-%m-%d')
            entry = record_map.get(date_str, {})

            print(f"\n[DEBUG] Checking Date: {date_str}")
            print(f"  → Entry: {entry}")

            time_in = entry.get("time_in")
            time_out = entry.get("time_out")
            
            has_time_in = bool(time_in)
            has_time_out = bool(time_out)
            
            if has_time_in and has_time_out:
                col_color = "#d4edda"  # ✅ light green if complete
            else:
                col_color = "#f8d7da"  # ❌ light red if incomplete

            # Apply color to ALL 12 rows of the current column
            for row in range(12):
                item = self.table.item(row, col)
                if not item:
                    item = QTableWidgetItem()
                    self.table.setItem(row, col, item)

                item.setBackground(QColor(col_color))
                item.setForeground(QColor("#000000"))

            # Handle Time In
            if time_in:
                print(f"  → Raw Time In: {time_in} ({type(time_in)})")
                try:
                    if isinstance(time_in, timedelta):
                        t_in = (datetime.min + time_in).time()
                    elif isinstance(time_in, str):
                        t_in = datetime.strptime(time_in, "%H:%M:%S").time()
                    elif isinstance(time_in, datetime):
                        t_in = time_in.time()
                    elif isinstance(time_in, datetime.time):
                        t_in = time_in
                    else:
                        raise ValueError(f"Unsupported time_in type: {type(time_in)}")

                    display_in = t_in.strftime("%I:%M %p")
                    in_hour = t_in.hour
                    row = in_hour - 7
                    if 0 <= row < 12:
                        item = self.table.item(row, col)
                        if not item:
                            item = QTableWidgetItem()
                            self.table.setItem(row, col, item)
                        existing_text = item.text()
                        new_text = (existing_text + f"\nIN: {display_in}").strip()
                        item.setText(new_text)

                except Exception as e:
                    print("[ERROR] parsing time_in:", e)

            # Handle Time Out
            if time_out:
                try:
                    t_out = (datetime.min + time_out).time()
                    out_hour = t_out.hour
                    row = out_hour - 7
                    if 0 <= row < 12:
                        display_out = t_out.strftime("%I:%M %p")
                        item = self.table.item(row, col)
                        if not item:
                            item = QTableWidgetItem()
                            self.table.setItem(row, col, item)
                        existing_text = item.text()
                        new_text = (existing_text + f"\nOUT: {display_out}").strip()
                        item.setText(new_text)

                        print(f"  → Time Out: {t_out} → Row: {row} → Display: {display_out}")
                except Exception as e:
                    print("[ERROR] parsing time_out:", e)
                
    def open_time_edit_dialog(self, row, column):
        item = self.table.item(row, column)

        # Don't proceed if the cell has existing data
        if item and item.text().strip():
            print("[INFO] Cell has data already, skipping edit.")
            return

        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Time Entry")

        layout = QVBoxLayout(dialog)
        label = QLabel("Add Time In or Time Out")
        layout.addWidget(label)

        time_edit = QTimeEdit()
        time_edit.setTime(datetime.now().time())
        time_edit.setDisplayFormat("hh:mm AP")
        layout.addWidget(time_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec():
            new_time = time_edit.time().toPython()
            formatted = datetime.combine(datetime.today(), new_time).strftime("%I:%M %p")

            # Let the user decide if it's Time In or Time Out
            type_dialog = QDialog(self)
            type_layout = QVBoxLayout(type_dialog)
            type_label = QLabel("Is this Time In or Time Out?")
            type_layout.addWidget(type_label)

            btn_in = QPushButton("Time In")
            btn_out = QPushButton("Time Out")

            selected = {"type": None}

            def choose_in():
                selected["type"] = "IN"
                type_dialog.accept()

            def choose_out():
                selected["type"] = "OUT"
                type_dialog.accept()

            btn_in.clicked.connect(choose_in)
            btn_out.clicked.connect(choose_out)

            type_layout.addWidget(btn_in)
            type_layout.addWidget(btn_out)

            if type_dialog.exec():
                time_type = selected["type"]
                if time_type:
                    new_label = f"{time_type}: {formatted}"
                    self.table.setItem(row, column, QTableWidgetItem(new_label))

                    # Compute actual date
                    from_date = self.from_date.date().toPython()
                    date_selected = from_date + timedelta(days=column)

                    # Format time as string
                    time_str = new_time.strftime('%H:%M:%S')

                    try:
                        db.submit_time_entry_request(self.employee_id, date_selected, time_type, time_str)

                        QMessageBox.information(self, "Request Sent",
                            f"Your {time_type.lower()} request for {date_selected.strftime('%Y-%m-%d')} at {formatted} "
                            "has been sent to the Admin for approval.")
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Failed to send request: {e}")
    
    def load_stylesheet(self):
        try:
            with open("styles/attendance_emp.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: styles/attendance_emp.qss not found.")

