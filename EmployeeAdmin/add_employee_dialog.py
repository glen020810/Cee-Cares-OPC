from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QFileDialog, QDateEdit, QTextEdit, QFrame, QWidget, QSizePolicy, QMessageBox
)
from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtGui import QPixmap, QFont, QIntValidator
import EmployeeAdmin.emp_admin_db as db  # o anong pangalan ng module mo
import os
import shutil

class AddEmployeeDialog(QDialog):
    employee_saved = Signal()
    
    def __init__(self, employee_data=None):
        super().__init__()
        self.setWindowTitle("Add / Edit Employee")
        self.employee_data = employee_data
        self.is_edit_mode = employee_data is not None

        from EmployeeAdmin.emp_admin_db import generate_employee_id

        self.setFixedSize(900, 600)
        self.load_stylesheet()

        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(20)

        # LEFT SIDE - Full Form Section
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(20, 0, 20, 0)

        title_label = QLabel("Employee Information")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignLeft)
        left_layout.addWidget(title_label)
        left_layout.addSpacing(5)

        # Grouped columns for clean layout
        row1_layout = QHBoxLayout()
        row2_layout = QHBoxLayout()
        row3_layout = QHBoxLayout()
        row4_layout = QHBoxLayout()
        row5_layout = QHBoxLayout()
        
        self.employee_id = QLineEdit()
        self.employee_id.setReadOnly(True)
        self.employee_id.setStyleSheet("background-color: #eee;")
        employee_id_layout = self._field("Employee ID:", self.employee_id)
        left_layout.addLayout(employee_id_layout)
        if not self.is_edit_mode:
            self.employee_id.setText(db.generate_employee_id())
        self.employee_id.setAlignment(Qt.AlignLeft)

        font = QFont("Segoe UI", 12)  # Palakihin font size
        font.setBold(True)
        self.employee_id.setFont(font)

        self.employee_id.setFixedHeight(40)  # Palakihin taas ng input box
        self.employee_id.setFixedWidth(200)

        self.employee_id.setStyleSheet("""
            QLineEdit {
            background-color: #f2f2f2;
            
            padding: 5px 10px;  /* bawasan yung padding kanan para lumawak */
            color: #333;
            font-weight: bold;
        }
    """)
        self.employee_id.setAlignment(Qt.AlignLeft)  

        # Row 1 - Last Name, First Name, Middle Name
        self.last_name = QLineEdit()
        self.first_name = QLineEdit()
        self.middle_name = QLineEdit()
        row1_layout.addLayout(self._field("Last Name:", self.last_name))
        row1_layout.addLayout(self._field("First Name:", self.first_name))
        row1_layout.addLayout(self._field("Middle Name:", self.middle_name))
        row1_layout.setSpacing(10)
        
        # Row 2 - Date of Birth, Gender, Place of Birth
        self.marital_status = QComboBox()
        self.marital_status.addItem("Select Marital Status")
        self.marital_status.addItems(["Single", "Married", "Widow", "Separated"])
        self.marital_status.setCurrentIndex(0)
        self.marital_status.setStyleSheet("color: gray;")
        self.marital_status.currentIndexChanged.connect(self.on_marital_status_changed)

        self.dob = QDateEdit()
        self.dob.setCalendarPopup(True)
        self.dob.setDisplayFormat("yyyy-MM-dd")
        self.dob.setSpecialValueText("Select Date")
        self.dob.setDateRange(QDate(1900, 1, 1), QDate(2100, 12, 31))
        self.dob.setDate(self.dob.minimumDate())  
        self.dob.dateChanged.connect(lambda _: self.on_date_changed(self.dob))
        self.dob.setStyleSheet("color: gray;")

        self.gender = QComboBox()
        self.gender.addItem("Select Gender")  # Placeholder
        self.gender.addItems(["Male", "Female"])
        self.gender.setCurrentIndex(0)  # Default to placeholder
        self.gender.currentIndexChanged.connect(self.on_gender_changed)
        self.gender.setCurrentIndex(0)
        self.gender.setStyleSheet("color: gray;")

        self.place_of_birth = QLineEdit()
        row2_layout.addLayout(self._field("Marital Status:", self.marital_status))
        row2_layout.addLayout(self._field("Date of Birth:", self.dob))
        row2_layout.addLayout(self._field("Gender:", self.gender))
        row2_layout.addLayout(self._field("Place of Birth:", self.place_of_birth))
        row2_layout.setSpacing(10)
        
        # Row 3 - Address, Contact No., Position
        self.address = QLineEdit()
        self.contact_no = QLineEdit()
        self.email = QLineEdit()
        self.position = QLineEdit()
        row3_layout.addLayout(self._field("Address:", self.address))
        row3_layout.addLayout(self._field("Contact No.:", self.contact_no))
        row3_layout.addLayout(self._field("Email Address:", self.email))
        row3_layout.setSpacing(8)
        self.contact_no.setValidator(QIntValidator())
        
        # Row 4 - SSS, TIN, Pag-IBIG, PhilHealth
        row4_layout = QHBoxLayout()
        self.sss_no = QLineEdit()
        self.tin_no = QLineEdit()
        self.pagibig_no = QLineEdit()
        self.philhealth_no = QLineEdit()
        row4_layout.addLayout(self._field("SSS No.:", self.sss_no))
        row4_layout.addLayout(self._field("TIN No.:", self.tin_no))
        row4_layout.addLayout(self._field("Pag-IBIG No.:", self.pagibig_no))
        row4_layout.addLayout(self._field("PhilHealth No.:", self.philhealth_no))
        row4_layout.setSpacing(10)
        self.sss_no.setValidator(QIntValidator())
        self.tin_no.setValidator(QIntValidator())
        self.pagibig_no.setValidator(QIntValidator())
        self.philhealth_no.setValidator(QIntValidator())


        # Row 4 - Hire Date
        
        self.hire_date = QDateEdit()
        self.hire_date.setCalendarPopup(True)
        self.hire_date.setDisplayFormat("yyyy-MM-dd")
        self.hire_date.setSpecialValueText("Select Date")
        self.hire_date.setDateRange(QDate(1900, 1, 1), QDate(2100, 12, 31))
        self.hire_date.setDate(self.hire_date.minimumDate())  # Set to "empty" value
        self.hire_date.dateChanged.connect(lambda _: self.on_date_changed(self.hire_date))
        self.hire_date.setStyleSheet("color: gray;")
        self.salary = QLineEdit()
        self.salary.setValidator(QIntValidator())  # Para numbers lang
        self.salary.setPlaceholderText("₱0.00")  # Placeholder Philippine Currency
        row5_layout.addLayout(self._field("Position:", self.position))
        row5_layout.addLayout(self._field("Hire Date:", self.hire_date))
        row5_layout.addLayout(self._field("Salary (₱):", self.salary))
        row5_layout.addStretch()
        row5_layout.setSpacing(10)

        
        # Add rows to left side
        left_layout.addSpacing(30)
        left_layout.addLayout(row1_layout)
        left_layout.addLayout(row2_layout)
        left_layout.addLayout(row3_layout)
        left_layout.addLayout(row4_layout)
        left_layout.addLayout(row5_layout)
        left_layout.addStretch()

        # RIGHT SIDE - Picture & Buttons
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignTop)
        
        self.pic_frame = QFrame()
        self.pic_frame.setObjectName("PictureFrame")
        self.pic_frame.setFixedSize(150, 150)
        
        self.pic_frame.setLayout(QVBoxLayout())
        self.pic_frame.layout().setContentsMargins(0, 0, 0, 0)


        self.attach_btn = QPushButton("Attach Picture")
        self.submit_btn = QPushButton("Save")
        right_layout.setContentsMargins(20, 0, 0, 0)
        right_layout.addSpacing(30)
        self.submit_btn.clicked.connect(self.save_employee)
    
        right_layout.addWidget(self.pic_frame, alignment=Qt.AlignCenter)
        right_layout.addWidget(self.attach_btn, alignment=Qt.AlignCenter)
        
        right_layout.addStretch()
        right_layout.addWidget(self.submit_btn)
        
        if not self.is_edit_mode:
            self.employee_id.setText(db.generate_employee_id())

        # Button label & signal depending on mode
        if self.is_edit_mode:
            self.load_employee_data()

            self.submit_btn.setText("Update")
            try:
                self.submit_btn.clicked.disconnect()
            except:
                pass
            self.submit_btn.clicked.connect(self.update_employee)
        else:
            self.submit_btn.setText("Save")
            try:
                self.submit_btn.clicked.disconnect()
            except:
                pass
            self.submit_btn.clicked.connect(self.save_employee)


        # Add to main layout
        main_layout.addLayout(left_layout, stretch=3)
        main_layout.addLayout(right_layout, stretch=1)

        self.attach_btn.clicked.connect(self.attach_picture)
        self.selected_image_path = None
        
        self.save_button = QPushButton("Update" if self.is_edit_mode else "Save")
        self.save_button.clicked.connect(self.update_employee if self.is_edit_mode else self.save_employee)

    def _field(self, label_text, widget):
        """Helper to return a VBox with label above widget."""
        layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold;")
        layout.addWidget(label)
        layout.addWidget(widget)
        container = QVBoxLayout()
        container.addLayout(layout)
        return container

    def attach_picture(self):
        file_path, _ = QFileDialog.getOpenFileName(
           self, "Select Picture", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file_path:
            print(f"Picture selected: {file_path}")
            pixmap = QPixmap(file_path)
            if pixmap.isNull():
                print("⚠️ Failed to load image.")
                return

            scaled_pixmap = pixmap.scaled(
                self.pic_frame.width(), self.pic_frame.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

            # Clear previous image from layout
            layout = self.pic_frame.layout()
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

            # Add new image to layout
            image_label = QLabel()
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(image_label)

            self.selected_image_path = file_path

    def save_employee(self):
        from EmployeeAdmin.emp_admin_db import insert_employee, generate_employee_id

        employee_id = self.employee_id.text()
        last_name = self.last_name.text().strip()
        first_name = self.first_name.text().strip()
        middle_name = self.middle_name.text().strip()
        marital_status = self.marital_status.currentText()
        gender = self.gender.currentText()
        dob = self.dob.date().toString("yyyy-MM-dd")
        place_of_birth = self.place_of_birth.text().strip()
        address = (
            self.address.toPlainText().strip()
            if isinstance(self.address, QTextEdit)
            else self.address.text().strip()
        )
        contact_no = self.contact_no.text().strip()
        email = self.email.text().strip()
        sss_no = self.sss_no.text().strip()
        tin_no = self.tin_no.text().strip()
        pagibig_no = self.pagibig_no.text().strip()
        philhealth_no = self.philhealth_no.text().strip()

        position = self.position.text().strip()
        hire_date = self.hire_date.date().toString("yyyy-MM-dd")
        salary = self.salary.text().strip()
        profile_image = getattr(self, "selected_image_path", None)
        if profile_image:
            images_dir = os.path.join(os.getcwd(), "images")
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)

            # Use the employee ID to generate a unique filename
            ext = os.path.splitext(profile_image)[1]
            new_filename = f"{employee_id}{ext}"
            destination = os.path.join(images_dir, new_filename)

            try:
                shutil.copy(profile_image, destination)
                profile_image = destination  # Update the variable to save correct path
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to copy image:\n{e}")
                return 


        errors = []
        if not last_name:
            errors.append("Last Name is required.")
        if not first_name:
            errors.append("First Name is required.")
        if marital_status == "Select Marital Status":
            errors.append("Please select Marital Status.")
        if gender == "Select Gender":
            errors.append("Please select Gender.")
        if self.dob.date() == self.dob.minimumDate():
            errors.append("Please select Date of Birth.")
        if not place_of_birth:
            errors.append("Place of Birth is required.")
        if not address:
            errors.append("Address is required.")
        if not contact_no:
            errors.append("Contact No. is required.")
        if not position:
            errors.append("Position is required.")
        if self.hire_date.date() == self.hire_date.minimumDate():
                errors.append("Please select Hire Date.")
        if not sss_no:
            errors.append("SSS No. is required.")
        if not tin_no:
            errors.append("TIN No. is required.")
        if not pagibig_no:  
            errors.append("Pag-IBIG No. is required.")
        if not philhealth_no:
            errors.append("PhilHealth No. is required.")
        if email and "@" not in email:
            errors.append("Invalid email address.")
        if not salary: errors.append("Salary is required.")

        if errors:
            QMessageBox.warning(self, "Missing Information", "\n".join(errors))
            return

        data = (
            employee_id,
            last_name, first_name, middle_name, marital_status, gender, dob,
            place_of_birth, address, contact_no, email, position,
            hire_date, salary, 
            sss_no, tin_no, pagibig_no, philhealth_no,
            profile_image,
        )

        try:
            insert_employee(data)
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save employee:\n{e}")
            return

        QMessageBox.information(self, "Success", "Employee saved successfully!")
        self.employee_id.setText(generate_employee_id())
        self.employee_saved.emit()  # ✅ Emit signal
        self.reset_fields()

    def reset_fields(self):
        self.last_name.clear()
        self.first_name.clear()
        self.middle_name.clear()
        self.marital_status.setCurrentIndex(0)  # Reset to "Select Marital Status"
        self.gender.setCurrentIndex(0)
        self.dob.setDate(self.dob.minimumDate())
        self.place_of_birth.clear()
    
        if isinstance(self.address, QTextEdit):
            self.address.clear()
        else:
            self.address.setText("")
    
        self.contact_no.clear()
        self.email.clear()
        self.sss_no.clear()
        self.tin_no.clear()
        self.pagibig_no.clear()
        self.philhealth_no.clear()
        self.position.clear()
        self.hire_date.setDate(self.hire_date.minimumDate())
        self.salary.clear()


        # Reset image path variable
        self.selected_image_path = None

        # Clear the picture preview inside pic_frame
        layout = self.pic_frame.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        # Optional: reset pic_frame style (border, background)
        self.pic_frame.setStyleSheet("border: 1px solid gray; background-color: white;")

    def load_employee_data(self):
        data = self.employee_data
        self.employee_id.setText(data['employee_id'])
        self.first_name.setText(data['first_name'])
        self.middle_name.setText(data['middle_name'])
        self.last_name.setText(data['last_name'])
        self.contact_no.setText(data['contact_no'])
        self.email.setText(data['email'])  # ✅ Added
        self.place_of_birth.setText(data['place_of_birth'])  # ✅ Added
        self.address.setText(data['address'])  # ✅ Added
        self.sss_no.setText(data.get("sss_no", ""))
        self.tin_no.setText(data.get("tin_no", ""))
        self.pagibig_no.setText(data.get("pagibig_no", ""))
        self.philhealth_no.setText(data.get("philhealth_no", ""))
        self.position.setText(data['position'])
        self.salary.setText(str(data.get('salary', '')))
        

        # Gender combo box
        gender_index = self.gender.findText(data['gender'])
        if gender_index >= 0:
            self.gender.setCurrentIndex(gender_index)
            self.on_gender_changed(gender_index)
        
        marital_status_index = self.marital_status.findText(data['marital_status'])
        if marital_status_index >= 0:
            self.marital_status.setCurrentIndex(marital_status_index)
            self.on_marital_status_changed(marital_status_index)

        # Dates
        if data['dob']:
            self.dob.setDate(QDate.fromString(data['dob'], "yyyy-MM-dd"))
            self.on_date_changed(self.dob)
        if data['hire_date']:
            self.hire_date.setDate(QDate.fromString(data['hire_date'], "yyyy-MM-dd"))
            self.on_date_changed(self.hire_date)

            # Picture
            self.selected_image_path = data['profile_image']
        if self.selected_image_path and os.path.exists(self.selected_image_path):
            pixmap = QPixmap(self.selected_image_path)
            scaled_pixmap = pixmap.scaled(
                self.pic_frame.width(), self.pic_frame.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            layout = self.pic_frame.layout()
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            label = QLabel()
            label.setPixmap(scaled_pixmap)
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

    def update_employee(self):
        data = {
            "employee_id": self.employee_id.text(),
            "first_name": self.first_name.text(),
            "middle_name": self.middle_name.text(),
            "last_name": self.last_name.text(),
            "marital_status": self.marital_status.currentText(),
            "gender": self.gender.currentText(),
            "dob": self.dob.date().toString("yyyy-MM-dd"),
            "place_of_birth": self.place_of_birth.text().strip(),
            "address": self.address.text().strip(),
            "contact_no": self.contact_no.text().strip(),
            "email": self.email.text().strip(),
            "sss_no": self.sss_no.text().strip(),
            "tin_no": self.tin_no.text().strip(),
            "pagibig_no": self.pagibig_no.text().strip(),
            "philhealth_no": self.philhealth_no.text().strip(),
            "position": self.position.text().strip(),
            "hire_date": self.hire_date.date().toString("yyyy-MM-dd"),
            "salary": self.salary.text().strip(),
            "profile_image": self.selected_image_path or self.employee_data.get('profile_image'),
        }

        try:
            db.update_employee(data)
            QMessageBox.information(self, "Updated", "Employee data has been updated.")
            self.employee_saved.emit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Update Failed", f"An error occurred:\n{e}")

    def on_gender_changed(self, index):
        if index > 0:
            self.gender.setStyleSheet("color: black;")
        else:
            self.gender.setStyleSheet("color: gray;")
            
    def on_date_changed(self, date_edit):
        if date_edit.date() > date_edit.minimumDate():
            date_edit.setStyleSheet("color: black;")
        else:
            date_edit.setStyleSheet("color: gray;")
            
    def on_marital_status_changed(self, index):
        if index > 0:
            self.marital_status.setStyleSheet("color: black;")
        else:
            self.marital_status.setStyleSheet("color: gray;")


    def load_stylesheet(self):
        try:
            with open("styles/add_employee.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: add_employee.qss not found")
