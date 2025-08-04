from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QHBoxLayout, QDateEdit, QComboBox, QTextEdit, QMessageBox,
    QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QFont, QColor, QStandardItemModel, QStandardItem
from PySide6.QtCore import QDate, Qt
import os
import EmployeeAdmin.emp_admin_db as db  # Adjust if needed

class LeavePage(QWidget):
    def __init__(self, employee_id):
        super().__init__()
        self.employee_id = employee_id
        self.setObjectName("LeaveRequestPage")
        self.load_stylesheet()
        self.init_ui()

    def init_ui(self):
        # Main layout: horizontal (for sidebar + content)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Add left spacer (gap between sidebar and content)
        main_layout.addSpacing(50)  # ← adjust based on sidebar width

        # Vertical layout to hold the white container
        content_wrapper = QVBoxLayout()
        content_wrapper.setAlignment(Qt.AlignTop)
        content_wrapper.setContentsMargins(0, 30, 50, 30)  # top/right/bottom margin

        # The white card container
        container = QFrame()
        container.setObjectName("LeaveRequestContainer")

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 160))
        container.setGraphicsEffect(shadow)

        # Inside the card
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(30, 30, 30, 30)
        container_layout.setSpacing(20)

        title_label = QLabel("Leave Application")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))

        container_layout.addWidget(title_label)
        self.build_form(container_layout)
        self.build_table(container_layout)
        container.setLayout(container_layout)

        content_wrapper.addWidget(container)
        main_layout.addLayout(content_wrapper)

        # Set the final layout to the page
        self.setLayout(main_layout)

        self.refresh_table()

    def build_form(self, parent_layout):
        form_layout = QHBoxLayout()

        # Leave Type ComboBox with disabled gray placeholder
        self.leave_type = QComboBox()
        type_model = QStandardItemModel()
        item = QStandardItem("Select Type")
        item.setEnabled(False)
        item.setForeground(QColor("gray"))
        type_model.appendRow(item)

        for option in ["Sick Leave", "Vacation Leave", "Emergency Leave"]:
            type_model.appendRow(QStandardItem(option))

        self.leave_type.setModel(type_model)
        self.leave_type.setCurrentIndex(0)

        # Paid Status ComboBox with disabled gray placeholder
        self.paid_status = QComboBox()
        payment_model = QStandardItemModel()
        item2 = QStandardItem("Select Payment")
        item2.setEnabled(False)
        item2.setForeground(QColor("gray"))
        payment_model.appendRow(item2)

        for option in ["Paid", "Unpaid"]:
            payment_model.appendRow(QStandardItem(option))

        self.paid_status.setModel(payment_model)
        self.paid_status.setCurrentIndex(0)
        
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())

        self.reason = QTextEdit()
        self.reason.setPlaceholderText("Reason for leave")
        self.reason.setFixedHeight(50)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.submit_request)

        form_layout.addWidget(QLabel("Type:"))
        form_layout.addWidget(self.leave_type)
        form_layout.addWidget(QLabel("Payment:"))
        form_layout.addWidget(self.paid_status)
        form_layout.addWidget(QLabel("From:"))
        form_layout.addWidget(self.start_date)
        form_layout.addWidget(QLabel("To:"))
        form_layout.addWidget(self.end_date)
        form_layout.addWidget(self.submit_btn)

        parent_layout.addLayout(form_layout)
        parent_layout.addWidget(self.reason)

    def build_table(self, parent_layout):
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Leave Type", "Payment", "Start", "End", "Reason", "Status", "Reviewed By"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        parent_layout.addWidget(self.table)

    def submit_request(self):
        leave_type = self.leave_type.currentText()
        paid_status = self.paid_status.currentText()
        start = self.start_date.date().toString("yyyy-MM-dd")
        end = self.end_date.date().toString("yyyy-MM-dd")
        reason = self.reason.toPlainText().strip()

        if self.leave_type.currentIndex() == 0:
            QMessageBox.warning(self, "Validation Error", "Please select a leave type.")
            return
        if self.paid_status.currentIndex() == 0:
            QMessageBox.warning(self, "Validation Error", "Please select a payment type.")
            return
        if not reason:
            QMessageBox.warning(self, "Validation Error", "Please enter a reason for your leave.")
            return

        try:
            # ✅ Make sure your DB function supports this extra param
            db.submit_leave_request(self.employee_id, leave_type, paid_status, start, end, reason)
            QMessageBox.information(self, "Success", "Leave request submitted.")
            self.reason.clear()
            self.leave_type.setCurrentIndex(0)
            self.paid_status.setCurrentIndex(0)
            self.refresh_table()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def refresh_table(self):
        try:
            leave_data = db.get_employee_leaves(self.employee_id)
            self.table.setRowCount(0)
            for row_data in leave_data:
                self.table.insertRow(self.table.rowCount())
                for col, val in enumerate(row_data):
                    self.table.setItem(self.table.rowCount() - 1, col, QTableWidgetItem(str(val)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unable to load leave requests:\n{str(e)}")

    def load_stylesheet(self):
        try:
            qss_path = os.path.join(os.path.dirname(__file__), "..", "styles", "leave_emp.qss")
            with open(os.path.abspath(qss_path), "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: styles/leave_emp.qss not found.")