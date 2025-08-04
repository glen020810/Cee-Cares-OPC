from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
import EmployeeAdmin.emp_admin_db as db
import os
from PayrollAdmin.payroll_form import PayrollFormDialog


class EnrollPayrollWindow(QDialog):
    def __init__(self, refresh_callback=None):
        super().__init__()
        self.refresh_callback = refresh_callback
        self.setWindowTitle("Enroll to Payroll")
        self.setModal(True) 
        self.setup_ui()
        self.setFixedSize(700, 450)

        self.setObjectName("EnrollPayrollWindow")

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 250)

        # Label, Input at Button sa iisang linya
        top_layout = QHBoxLayout()
        top_layout.setSpacing(50)

        id_label = QLabel("Enter Employee ID:")
        self.id_input = QLineEdit()
        self.generate_btn = QPushButton("Generate")  # Importanteng mauna to

        top_layout.addWidget(id_label)
        top_layout.addWidget(self.id_input)
        top_layout.addWidget(self.generate_btn)

        self.generate_btn.clicked.connect(self.generate_employee)

        # Result Table
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(["Employee ID", "Name", "Salary"])
        self.result_table.setRowCount(0)
        self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setMaximumHeight(100)
        self.result_table.setColumnWidth(0, 178)  # Employee ID
        self.result_table.setColumnWidth(1, 300)  # Name
        self.result_table.setColumnWidth(2, 200)  # Salary
        self.result_table.setFocusPolicy(Qt.NoFocus)
        self.result_table.setSelectionMode(QTableWidget.NoSelection)
        self.result_table.cellClicked.connect(self.on_table_cell_clicked)


        # Add layouts
        layout.addLayout(top_layout)
        layout.addWidget(self.result_table) 

        self.load_stylesheet()
        

    def setup_ui(self):
        # layout at iba pang UI code mo
        pass
    
    def load_stylesheet(self):
        try:
            with open("styles/enroll_payroll.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: payroll.qss not found. Default style applied.")

    def generate_employee(self):
        emp_id = self.id_input.text().strip()

        if not emp_id:
            QMessageBox.warning(self, "Error", "Please enter a valid Employee ID.")
            return

        employee = db.get_employee_by_id(emp_id)
        print(f"DEBUG - Employee fetched: {employee}")

        if employee:
            full_name = f"{employee['first_name']} {employee['middle_name']} {employee['last_name']}".strip()

            self.result_table.setRowCount(1)
            self.result_table.setRowHeight(0, 120)

            item_id = QTableWidgetItem(employee['employee_id'])
            item_id.setTextAlignment(Qt.AlignCenter)
            self.result_table.setItem(0, 0, item_id)

            name_widget = QWidget()
            name_layout = QHBoxLayout(name_widget)
            name_layout.setContentsMargins(0, 0, 0, 48)
            name_layout.setSpacing(15)
            name_layout.setAlignment(Qt.AlignCenter)

            photo_label = QLabel()
            if employee['profile_image'] and os.path.exists(employee['profile_image']):
                pixmap = QPixmap(employee['profile_image']).scaled(40, 40, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

                size = min(pixmap.width(), pixmap.height())
                mask = QPixmap(size, size)
                mask.fill(Qt.transparent)

                painter = QPainter(mask)
                painter.setRenderHint(QPainter.Antialiasing)
                path = QPainterPath()
                path.addEllipse(0, 0, size, size)
                painter.setClipPath(path)
                painter.drawPixmap(0, 0, pixmap)
                painter.end()

                photo_label.setPixmap(mask)
            else:
                photo_label.setText("🖼️")
                photo_label.setAlignment(Qt.AlignCenter)

            name_label = QLabel(full_name)
            name_layout.addWidget(photo_label)
            name_layout.addWidget(name_label)

            self.result_table.setCellWidget(0, 1, name_widget)

            item_salary = QTableWidgetItem(str(employee['salary']))
            item_salary.setTextAlignment(Qt.AlignCenter)
            self.result_table.setItem(0, 2, item_salary)

            header = self.result_table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        else:
            QMessageBox.information(self, "Not Found", "Employee not found.")
            self.result_table.setRowCount(0)

            
    def clear_payroll_form(self):
        
            self.allowance_input.clear()
            self.overtime_days_input.clear()
            self.overtime_hours_input.clear()
            self.overtime_amount_input.clear()
            self.restday_pay_input.clear()
            self.reg_holiday_pay_input.clear()
            self.sp_holiday_pay_input.clear()
            self.other_earnings_input.clear()

            self.late_input.clear()
            self.sss_input.clear()
            self.philhealth_input.clear()
            self.pagibig_input.clear()
            self.loan_input.clear()
            self.others_input.clear()

            self.gross_salary_display.setText("₱0.00")
            self.total_deductions_display.setText("₱0.00")
            self.net_salary_display.setText("₱0.00")
            
    def on_table_cell_clicked(self, row, column):
        if column == 1:  # Clicked Name
            emp_id_item = self.result_table.item(row, 0)
            if emp_id_item:
                emp_id = emp_id_item.text()
                employee = db.get_employee_by_id(emp_id)
                if employee:
                    basic_salary = float(employee['salary'])
                    form = PayrollFormDialog(employee, basic_salary)
                    form.exec()

                    if self.refresh_callback:
                        self.refresh_callback()







