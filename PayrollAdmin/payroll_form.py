from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout
)
from PySide6.QtCore import Qt, Signal
from datetime import datetime
import EmployeeAdmin.emp_admin_db as db


class PayrollFormDialog(QDialog):
    payroll_submitted = Signal()

    def __init__(self, employee, basic_salary, time_entries=None):
        super().__init__()
        self.setWindowTitle("Payroll Form")
        self.setFixedSize(400, 650)
        self.employee = employee
        self.basic_salary = basic_salary
        self.time_entries = time_entries or []
        self.payroll_data = {}

        # Load payroll profile data
        self.profile_data = db.get_payroll_profile(self.employee['employee_id']) or {}

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"<b>Payroll for: {self.employee['first_name']} {self.employee['last_name']}</b>"))
        layout.addWidget(QLabel(f"<b>Basic Salary:</b> ₱{self.basic_salary:,.2f}"))

        self.cutoff_label = QLabel("<i>Cutoff Period: July 1 – July 15, 2025</i>")
        layout.addWidget(self.cutoff_label)

        self.attendance_summary = QLabel("Present: 0 | Absent: 0 | Late: 0 mins | Undertime: 0 mins")
        layout.addWidget(self.attendance_summary)

        # === ADDITIONAL EARNINGS ===
        layout.addWidget(QLabel("<b>ADDITIONAL EARNINGS</b>"))
        add_grid = QGridLayout()
        self.allowance_input = QLineEdit()
        self.allowance_input.setText(str(self.profile_data.get('allowance', 0)))
        self.overtime_amount_display = QLabel("₱0.00")

        add_grid.addWidget(QLabel("Allowance:"), 0, 0)
        add_grid.addWidget(self.allowance_input, 0, 1)
        add_grid.addWidget(QLabel("Overtime Amount:"), 1, 0)
        add_grid.addWidget(self.overtime_amount_display, 1, 1)
        layout.addLayout(add_grid)

        self.gross_salary_display = QLabel("Gross Salary: ₱0.00")
        layout.addWidget(self.gross_salary_display)

        # === DEDUCTIONS ===
        layout.addWidget(QLabel("<b>DEDUCTIONS</b>"))
        ded_grid = QGridLayout()

        self.late_input = QLineEdit()
        self.late_input.setPlaceholderText("Auto-computed from attendance")
        self.late_input.setReadOnly(True)

        self.sss_input = QLineEdit()
        self.sss_input.setText(str(self.profile_data.get('sss', 0)))

        self.philhealth_input = QLineEdit()
        self.philhealth_input.setText(str(self.profile_data.get('philhealth', 0)))

        self.pagibig_input = QLineEdit()
        self.pagibig_input.setText(str(self.profile_data.get('pagibig', 0)))

        self.loan_input = QLineEdit()
        self.loan_input.setText(str(self.profile_data.get('loan', 0)))

        self.others_input = QLineEdit()
        self.others_input.setText(str(self.profile_data.get('other_deductions', 0)))

        ded_grid.addWidget(QLabel("Late/Undertime:"), 0, 0)
        ded_grid.addWidget(self.late_input, 0, 1)
        ded_grid.addWidget(QLabel("SSS:"), 1, 0)
        ded_grid.addWidget(self.sss_input, 1, 1)
        ded_grid.addWidget(QLabel("PhilHealth:"), 2, 0)
        ded_grid.addWidget(self.philhealth_input, 2, 1)
        ded_grid.addWidget(QLabel("Pag-IBIG:"), 3, 0)
        ded_grid.addWidget(self.pagibig_input, 3, 1)
        ded_grid.addWidget(QLabel("Loan:"), 4, 0)
        ded_grid.addWidget(self.loan_input, 4, 1)
        ded_grid.addWidget(QLabel("Other Deductions:"), 5, 0)
        ded_grid.addWidget(self.others_input, 5, 1)
        layout.addLayout(ded_grid)

        self.total_deductions_display = QLabel("Total Deductions: ₱0.00")
        layout.addWidget(self.total_deductions_display)

        # === NET SALARY ===
        net_layout = QHBoxLayout()
        net_layout.addWidget(QLabel("<b>NET SALARY:</b>"))
        self.net_salary_display = QLabel("₱0.00")
        net_layout.addWidget(self.net_salary_display)
        layout.addLayout(net_layout)

        # === Buttons ===
        compute_btn = QPushButton("Compute Payroll")
        compute_btn.clicked.connect(self.compute_payroll)
        layout.addWidget(compute_btn)

        submit_btn = QPushButton("Submit Payroll")
        submit_btn.clicked.connect(self.submit_payroll)
        layout.addWidget(submit_btn)

    def compute_payroll(self):
        try:
            overtime_amount = self.calculate_overtime_amount(self.time_entries)
            self.overtime_amount_display.setText(f"₱{overtime_amount:,.2f}")

            allowance = float(self.allowance_input.text() or 0)
            late = float(self.late_input.text() or 0)
            sss = float(self.sss_input.text() or 0)
            philhealth = float(self.philhealth_input.text() or 0)
            pagibig = float(self.pagibig_input.text() or 0)
            loan = float(self.loan_input.text() or 0)
            others = float(self.others_input.text() or 0)

            gross_salary = self.basic_salary + allowance + overtime_amount
            total_deductions = late + sss + philhealth + pagibig + loan + others
            net_salary = gross_salary - total_deductions

            self.gross_salary_display.setText(f"Gross Salary: ₱{gross_salary:,.2f}")
            self.total_deductions_display.setText(f"Total Deductions: ₱{total_deductions:,.2f}")
            self.net_salary_display.setText(f"₱{net_salary:,.2f}")

            self.payroll_data = {
                'employee_id': self.employee['employee_id'],
                'period_start': '2025-07-01',
                'period_end': '2025-07-15',
                'basic_salary': self.basic_salary,
                'allowance': allowance,
                'overtime_pay': overtime_amount,
                'gross_salary': gross_salary,
                'late_deduction': late,
                'sss': sss,
                'philhealth': philhealth,
                'pagibig': pagibig,
                'loan': loan,
                'other_deductions': others,
                'total_deductions': total_deductions,
                'net_salary': net_salary,
                'processed_by': 'Admin'
            }

            QMessageBox.information(self, "Computed", "Payroll computation successful.")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers in all fields.")

    def submit_payroll(self):
        if not self.payroll_data:
            QMessageBox.warning(self, "Missing Data", "Please compute payroll first.")
            return
        try:
            db.save_payroll_record(self.payroll_data)

            # 🔽 Ito ang kailangan mong idagdag:
            db.save_or_update_payroll_profile(self.payroll_data)

            db.register_payroll_profile(self.payroll_data['employee_id'])
            QMessageBox.information(self, "Submitted", "Payroll saved successfully.")
    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Submission failed:\n{str(e)}")
            
            self.payroll_submitted.emit()
            self.accept()

    def calculate_overtime_amount(self, time_entries):
        hourly_rate = self.basic_salary / (22 * 8)
        total_minutes = 0
        cutoff_time = datetime.strptime("18:00", "%H:%M")

        for entry in time_entries:
            if not entry.get("approved", False):
                continue
            time_in_str = entry.get("time_in")
            time_out_str = entry.get("time_out")
            if not time_in_str or not time_out_str:
                continue

            time_in = datetime.strptime(time_in_str, "%H:%M")
            time_out = datetime.strptime(time_out_str, "%H:%M")

            if time_in > cutoff_time:
                overtime = (time_out - time_in).seconds // 60
                total_minutes += overtime

        total_hours = total_minutes / 60
        return total_hours * hourly_rate
