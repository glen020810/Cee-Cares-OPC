from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt, Signal
from PayrollAdmin.view_profile_dialog import ViewPayrollProfileDialog
from PayrollAdmin.edit_profile_dialog import EditPayrollProfileDialog
import EmployeeAdmin.emp_admin_db as db  # Assumes you have a function to get registered profiles
from PayrollAdmin.payroll_form import PayrollFormDialog
from PayrollAdmin.enroll_payroll import EnrollPayrollWindow

from functools import partial



class PayrollProfileListWindow(QWidget):
    refresh_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registered Payroll Profiles")
        self.setFixedSize(800, 500)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(50, 10, 20, 10)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Employee ID", "Name", "Position", "Hire Date", "Salary", "Action"])
        self.table.verticalHeader().setVisible(False)
        self.layout.addWidget(self.table)
        
        self.refresh_requested.connect(self.load_profiles)
        self.table.cellDoubleClicked.connect(self.open_profile_dialog)

        self.load_profiles()

    def load_profiles(self):
        print("[INFO] Reloading profiles...")

        self.table.setRowCount(0)
        profiles = db.get_all_registered_profiles()
        print(f"[INFO] Found {len(profiles)} profiles")

        
        for row_idx, profile in enumerate(profiles):
            self.table.insertRow(row_idx)

            self.table.setItem(row_idx, 0, QTableWidgetItem(profile['employee_id']))

            name_item = QTableWidgetItem(f"{profile['first_name']} {profile['last_name']}")
            name_item.setForeground(Qt.blue)
            name_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(row_idx, 1, name_item)

            self.table.setItem(row_idx, 2, QTableWidgetItem(profile['position']))
            self.table.setItem(row_idx, 3, QTableWidgetItem(profile['hire_date'].strftime("%Y-%m-%d")))
            self.table.setItem(row_idx, 4, QTableWidgetItem(f"₱{profile['salary']:,.2f}"))

            # Action buttons
            btn_layout = QHBoxLayout()
            edit_btn = QPushButton("Edit")
            delete_btn = QPushButton("Delete")
            
            edit_btn.clicked.connect(partial(self.edit_profile, profile['employee_id']))
            delete_btn.clicked.connect(partial(self.delete_profile, profile['employee_id']))

            container = QWidget()
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)
            container.setLayout(btn_layout)
            self.table.setCellWidget(row_idx, 5, container)

    def open_profile_dialog(self, row, column):
        if column == 1:  # Name clicked
            emp_id = self.table.item(row, 0).text()
            dialog = ViewPayrollProfileDialog(emp_id)
            dialog.exec()

    def edit_profile(self, emp_id):
        dialog = EditPayrollProfileDialog(emp_id)
        dialog.exec()
        self.load_profiles()

    def delete_profile(self, employee_id):
        confirm = QMessageBox.question(self, "Delete", f"Delete payroll profile of {employee_id}?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            print(f"[DEBUG] Attempting to delete payroll profile for: {employee_id}")  # <-- DEBUG print
            
            deleted = db.delete_payroll_profile(employee_id)
            print(f"[DEBUG] Deleted rows: {deleted}")  # <-- Show if something was actually deleted

            if deleted:
                QMessageBox.information(self, "Deleted", f"Deleted profile for {employee_id}")
            else:
                QMessageBox.warning(self, "Not Found", f"No payroll profile found for {employee_id}")

            self.load_profiles()
            
    def open_enroll_dialog(self):
        dialog = EnrollPayrollWindow(refresh_callback=self.load_profiles)
        dialog.exec()
