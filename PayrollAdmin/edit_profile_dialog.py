from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
import EmployeeAdmin.emp_admin_db as db  # Adjust to where db functions are

class EditPayrollProfileDialog(QDialog):
    def __init__(self, employee_id):
        super().__init__()
        self.setWindowTitle("Edit Payroll Profile")
        self.setFixedSize(350, 300)
        self.employee_id = employee_id

        self.setup_ui()
        self.load_profile()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.inputs = {}
        fields = [
            ("Allowance", "allowance"),
            ("SSS", "sss"),
            ("PhilHealth", "philhealth"),
            ("Pag-IBIG", "pagibig"),
            ("Loan", "loan"),
            ("Other Deductions", "other_deductions")
        ]

        grid = QGridLayout()
        for i, (label, key) in enumerate(fields):
            grid.addWidget(QLabel(label + ":"), i, 0)
            self.inputs[key] = QLineEdit()
            grid.addWidget(self.inputs[key], i, 1)

        layout.addLayout(grid)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_profile)
        layout.addWidget(self.save_btn)

    def load_profile(self):
        profile = db.get_payroll_profile(self.employee_id)
        if profile:
            for key, field in self.inputs.items():
                field.setText(str(profile.get(key, 0)))
        else:
            # Blank inputs if no record found (initial add)
            for field in self.inputs.values():
                field.setText("0.00")

    def save_profile(self):
        try:
            data = {
                "employee_id": self.employee_id,
                "allowance": float(self.inputs["allowance"].text()),
                "sss": float(self.inputs["sss"].text()),
                "philhealth": float(self.inputs["philhealth"].text()),
                "pagibig": float(self.inputs["pagibig"].text()),
                "loan": float(self.inputs["loan"].text()),
                "other_deductions": float(self.inputs["other_deductions"].text())
            }

            db.save_or_update_payroll_profile(data)
            QMessageBox.information(self, "Saved", "Payroll profile updated successfully.")
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numeric values.")