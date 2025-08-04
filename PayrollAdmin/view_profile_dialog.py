from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
import EmployeeAdmin.emp_admin_db as db
from datetime import datetime

def safe_currency(value):
    """Format value as currency or default to ₱0.00"""
    try:
        return f"₱{float(value):,.2f}"
    except (TypeError, ValueError):
        return "₱0.00"

class ViewPayrollProfileDialog(QDialog):
    def __init__(self, employee_id):
        super().__init__()
        self.setWindowTitle("Payroll Profile")
        self.setFixedSize(400, 400)
        layout = QVBoxLayout(self)

        print(f"[DEBUG] Fetching profile for employee_id: {employee_id}")
        profile = db.get_payroll_profile(employee_id)
        print("[DEBUG] Profile fetched:", profile)
        employee = db.get_employee_by_id(employee_id)

        print(f"[DEBUG] Profile: {profile}")
        print(f"[DEBUG] Employee: {employee}")
        
        print(f"[DEBUG] Looking up employee_id: {employee_id}")
        print(f"[DEBUG] get_employee_by_id: {db.get_employee_by_id(employee_id)}")
        print(f"[DEBUG] get_payroll_profile: {db.get_payroll_profile(employee_id)}")

        if not profile or not employee:
            layout.addWidget(QLabel("Profile not found."))
            return

        # Format hire date
        hire_date = employee['hire_date']
        if isinstance(hire_date, datetime):
            hire_date_str = hire_date.strftime("%Y-%m-%d")
        else:
            hire_date_str = str(hire_date)

        # Name and header
        name_label = QLabel(f"<b>{employee['first_name']} {employee['last_name']}</b> ({employee_id})")
        name_label.setTextFormat(Qt.RichText)
        layout.addWidget(name_label)

        layout.addWidget(QLabel(f"Position: {employee['position']}"))
        layout.addWidget(QLabel(f"Hire Date: {hire_date_str}"))
        layout.addWidget(QLabel(f"Basic Salary: {safe_currency(employee['salary'])}"))

        # Additional Earnings
        header1 = QLabel("<hr><b>ADDITIONAL EARNINGS</b>")
        header1.setTextFormat(Qt.RichText)
        layout.addWidget(header1)

        layout.addWidget(QLabel(f"Allowance: {safe_currency(profile.get('allowance'))}"))

        # Deductions
        header2 = QLabel("<b>DEDUCTIONS</b>")
        header2.setTextFormat(Qt.RichText)
        layout.addWidget(header2)

        layout.addWidget(QLabel(f"SSS: {safe_currency(profile.get('sss'))}"))
        layout.addWidget(QLabel(f"PhilHealth: {safe_currency(profile.get('philhealth'))}"))
        layout.addWidget(QLabel(f"Pag-IBIG: {safe_currency(profile.get('pagibig'))}"))
        layout.addWidget(QLabel(f"Loan: {safe_currency(profile.get('loan'))}"))
        layout.addWidget(QLabel(f"Other Deductions: {safe_currency(profile.get('other_deductions'))}"))
