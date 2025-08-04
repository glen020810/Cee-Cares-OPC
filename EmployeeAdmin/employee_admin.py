from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QGraphicsDropShadowEffect, QLabel, QStyledItemDelegate, QStyle, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QIcon, QPainter, QPainterPath
from EmployeeAdmin.add_employee_dialog import AddEmployeeDialog

import EmployeeAdmin.emp_admin_db as db
from PySide6.QtGui import QPixmap  # for image
import os  

class NoFocusDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if option.state & QStyle.State_Selected:
            # Remove the selected state to prevent background drawing
            option.state = option.state & ~QStyle.State_Selected
        super().paint(painter, option, index)

class EmployeePage(QWidget):
    def __init__(self):
        super().__init__()

        self.load_stylesheet()

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(50, 30, 50, 30)

        # Floating container frame
        container = QFrame()
        container.setObjectName("EmployeeContainer")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)

        # Shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 160))

        container.setGraphicsEffect(shadow)
        

        # Top bar - Search and Filter
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search Employee")
        self.search_box.textChanged.connect(self.search_employees)
        self.filter_box = QComboBox()
        self.filter_box.addItems(["Active", "Inactive"])

        self.add_btn = QPushButton("Add Employee")
        self.add_btn.setFixedSize(120, 30)
        self.add_btn.setObjectName("addEmployeeBtn")
        self.add_btn.clicked.connect(self.show_add_dialog)

        top_bar.addWidget(self.search_box)
        top_bar.addWidget(self.filter_box)
        top_bar.addStretch()
        top_bar.addWidget(self.add_btn)
        
        self.filter_box.currentIndexChanged.connect(self.load_employees)

        container_layout.addLayout(top_bar)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "Position", "Contact", "Hire Date", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(60)  # Default row height, adjust mo depende sa gusto mo
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setItemDelegateForColumn(5, NoFocusDelegate(self.table))

        container_layout.addWidget(self.table)

        main_layout.addWidget(container)
        
        self.load_employees()
        
        header = self.table.horizontalHeader()
    
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Name auto size
        
        
    def load_employees(self):
        self.table.setRowCount(0)
        status = self.filter_box.currentText()  # 'Active' or 'Inactive'
        fetched_data = db.fetch_employees_by_status(status)
        for row in fetched_data:
            # same as before, unpack row and add to table
            employee_id = row[1]  # adjust index based on your schema
            last = row[2]
            first = row[3]
            middle = row[4]
            position = row[12]
            contact = row[10]
            hire_date = row[13]
            profile_image = row[15]

            middle_initial = f"{middle[0]}." if middle else ""
            full_name = f"{first} {middle_initial} {last}"

            self.add_table_row(employee_id, profile_image, full_name, position, contact, hire_date)

    def add_table_row(self, employee_id, profile_image, name, position, contact, hire_date):
        row = self.table.rowCount()
        self.table.insertRow(row)

        # Column 0: Employee ID
        self.table.setItem(row, 0, QTableWidgetItem(employee_id))

        # Column 1: Picture + Clickable Name
        name_widget = QWidget()
        layout = QHBoxLayout(name_widget)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(10)
        name_widget.setStyleSheet("background-color: transparent;")

        pic_label = QLabel()
        if profile_image and os.path.exists(profile_image):
            pixmap = QPixmap(profile_image).scaled(40, 40, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

            # Gumawa ng circular mask
            size = min(pixmap.width(), pixmap.height())
            mask = QPixmap(size, size)
            mask.fill(Qt.transparent)

            painter = QPainter(mask)
            painter.setRenderHint(QPainter.Antialiasing)
            path = QPainterPath()
            path.addEllipse(0, 0, size, size)
            painter.setClipPath(path)
            # I-draw ang pixmap sa loob ng circular path (mask)
            painter.drawPixmap(0, 0, pixmap)
            painter.end()

            pic_label.setPixmap(mask)
        else:
            pic_label.setText("🖼️")


        name_label = QLabel(f"<a href='#'>{name}</a>")
        name_label.setStyleSheet("""
            QLabel {
                color: #2a6fdb;
                font-weight: bold;
                background-color: transparent;
            }
            QLabel:hover {
                text-decoration: underline;
            }
        """)
        name_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        name_label.setOpenExternalLinks(False)
        name_label.linkActivated.connect(lambda _: self.on_name_clicked(employee_id))

        layout.addWidget(pic_label)
        layout.addWidget(name_label)
        layout.addStretch()

        self.table.setCellWidget(row, 1, name_widget)

        # Column 2: Position
        self.table.setItem(row, 2, QTableWidgetItem(position))
        # Column 3: Contact
        self.table.setItem(row, 3, QTableWidgetItem(contact))
        # Column 4: Hire Date
        self.table.setItem(row, 4, QTableWidgetItem(str(hire_date)))


        # Column 5: Actions
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(5)
        actions_layout.setAlignment(Qt.AlignCenter) 

        edit_btn = QPushButton()
        edit_btn.setObjectName("iconButton")
        edit_btn.setIcon(QIcon("icons/edit.png"))
        edit_btn.setToolTip("Edit Employee")
        edit_btn.setCursor(Qt.PointingHandCursor)
        edit_btn.clicked.connect(lambda checked, eid=employee_id: self.edit_employee(eid))

        delete_btn = QPushButton()
        delete_btn.setObjectName("iconButton")
        delete_btn.setIcon(QIcon("icons/delete.png"))
        delete_btn.setToolTip("Delete Employee")
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.clicked.connect(lambda checked, eid=employee_id: self.delete_employee(eid))


        actions_layout.addWidget(edit_btn)
        actions_layout.addWidget(delete_btn)

        self.table.setCellWidget(row, 5, actions_widget)

    def on_name_clicked(self, employee_id):
        from EmployeeAdmin.employee_profile_dialog import EmployeeProfileDialog
        employee = db.get_employee_by_id(employee_id)
        if employee:
            dialog = EmployeeProfileDialog(employee)
            dialog.exec()

    def show_add_dialog(self):
        dialog = AddEmployeeDialog()
        if dialog.exec():
            print("Employee Saved")
            self.load_employees()

    def load_stylesheet(self):
        try:
            with open("styles/employee.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: styles/employee.qss not found.")

        
    def delete_employee(self, employee_id):
        confirm = QMessageBox.question(
            self,
            "Delete Employee",
            f"Are you sure you want to delete employee {employee_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            # Call database function
            db.delete_employee(employee_id)

            # Refresh the table
            self.load_employees()

            # Optional: Success message
            QMessageBox.information(self, "Deleted", f"Employee {employee_id} has been deleted.")


    def show_add_dialog(self):
        dialog = AddEmployeeDialog()
        dialog.employee_saved.connect(self.load_employees)  # ✅ Connect the signal
        dialog.exec()  # Display the dialog (modal)
        
    def edit_employee(self, employee_id):
        from EmployeeAdmin.add_employee_dialog import AddEmployeeDialog  # local import to avoid circular import
        employee = db.get_employee_by_id(employee_id)
        if employee:
            dialog = AddEmployeeDialog(employee_data=employee)
            dialog.employee_saved.connect(self.load_employees)
            dialog.exec()
            
    def search_employees(self, text):
        keyword = text.lower().strip()
        status = self.filter_box.currentText()  # "Active" or "Inactive"
        self.table.setRowCount(0)

        
        all_employees = db.fetch_employees_by_status(status)

        for row in all_employees:
            employee_id = row[1]
            last = row[2]
            first = row[3]
            middle = row[4]
            position = row[11]
            contact = row[9]
            hire_date = row[12]
            profile_image = row[13]

            middle_initial = f"{middle[0]}." if middle else ""
            full_name = f"{first} {middle_initial} {last}".lower()

            if keyword in employee_id.lower() or keyword in full_name:
                self.add_table_row(employee_id, profile_image, f"{first} {middle_initial} {last}", position, contact, hire_date)

    def load_stylesheet(self):
        try:
            with open("styles/employee.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: styles/employee.qss not found.")


