from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt
import os
from EmployeeAdmin import emp_admin_db  # Adjust as needed


class PersonalInfoPage(QWidget):
    def __init__(self, employee_id=""):
        super().__init__()
        self.employee_id = employee_id

        self.init_ui()
        self.load_stylesheet()
        self.load_employee_info()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setSpacing(15)

        # Container with shadow
        container = QFrame()
        container.setObjectName("containerFrame")
        container.setStyleSheet("background-color: white; border-radius: 5px;")
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 120))
        container.setGraphicsEffect(shadow)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(30, 30, 30, 30)
        container_layout.setSpacing(8)

        # Top Layout: Title + Picture
        top_layout = QHBoxLayout()

        title = QLabel("Personal Information")
        title.setObjectName("titleLabel")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        top_layout.addWidget(title)
        top_layout.addStretch()

        self.picture_label = QLabel()
        self.picture_label.setObjectName("pictureLabel")
        self.picture_label.setFixedSize(140, 140)
        self.picture_label.setStyleSheet("border: 1px solid gray;")
        self.picture_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self.picture_label)

        container_layout.addLayout(top_layout)

        # Row 1: Names
        row1 = QHBoxLayout()
        self.last_name = QLineEdit(); self.last_name.setReadOnly(True)
        self.first_name = QLineEdit(); self.first_name.setReadOnly(True)
        self.middle_name = QLineEdit(); self.middle_name.setReadOnly(True)
        row1.addLayout(self._field("Last Name:", self.last_name))
        row1.addLayout(self._field("First Name:", self.first_name))
        row1.addLayout(self._field("Middle Name:", self.middle_name))
        container_layout.addLayout(row1)

        # Row 2: Status / Gender / Birthday
        row2 = QHBoxLayout()
        self.marital_status = QLineEdit(); self.marital_status.setReadOnly(True)
        self.gender = QLineEdit(); self.gender.setReadOnly(True)
        self.dob = QLineEdit(); self.dob.setReadOnly(True)
        row2.addLayout(self._field("Marital Status:", self.marital_status))
        row2.addLayout(self._field("Gender:", self.gender))
        row2.addLayout(self._field("Date of Birth:", self.dob))
        container_layout.addLayout(row2)

        # Row 3: Birth place / Address / Contact
        row3 = QHBoxLayout()
        self.birth_place = QLineEdit(); self.birth_place.setReadOnly(True)
        self.address = QLineEdit(); self.address.setReadOnly(True)
        self.contact_no = QLineEdit(); self.contact_no.setReadOnly(True)
        row3.addLayout(self._field("Place of Birth:", self.birth_place))
        row3.addLayout(self._field("Address:", self.address))
        row3.addLayout(self._field("Contact No.:", self.contact_no))
        container_layout.addLayout(row3)

        # Row 4: Email / Position / Hire date
        row4 = QHBoxLayout()
        self.email = QLineEdit(); self.email.setReadOnly(True)
        self.sss_no = QLineEdit(); self.sss_no.setReadOnly(True)
        self.tin_no = QLineEdit(); self.tin_no.setReadOnly(True)
        row4.addLayout(self._field("Email:", self.email))
        row4.addLayout(self._field("SSS No.:", self.sss_no))
        row4.addLayout(self._field("TIN No.:", self.tin_no))
        container_layout.addLayout(row4)

        # Row 5: SSS / TIN / PAG-IBIG / PhilHealth
        row5 = QHBoxLayout()
        self.pagibig_no = QLineEdit(); self.pagibig_no.setReadOnly(True)
        self.philhealth_no = QLineEdit(); self.philhealth_no.setReadOnly(True)
        self.position = QLineEdit(); self.position.setReadOnly(True)
        self.hire_date = QLineEdit(); self.hire_date.setReadOnly(True)
        row5.addLayout(self._field("PAG-IBIG No.:", self.pagibig_no))
        row5.addLayout(self._field("PhilHealth No.:", self.philhealth_no))
        row5.addLayout(self._field("Position:", self.position))
        row5.addLayout(self._field("Hire Date:", self.hire_date))
        container_layout.addLayout(row5)

        # Row 6: Salary
        row6 = QHBoxLayout()
        self.salary = QLineEdit(); self.salary.setReadOnly(True)
        row6.addLayout(self._field("Salary (₱):", self.salary))
        row6.addStretch()
        container_layout.addLayout(row6)

        container_layout.addStretch()
        main_layout.addWidget(container)

    def _field(self, label_text, widget):
        layout = QVBoxLayout()
        lbl = QLabel(label_text)
        lbl.setStyleSheet("font-weight: bold;")
        layout.addWidget(lbl)
        layout.addWidget(widget)
        return layout

    def load_stylesheet(self):
        try:
            with open("styles/personal_info_emp.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: personal_info_emp.qss not found")

    def load_employee_info(self):
        data = emp_admin_db.get_employee_by_id(self.employee_id)
        if not data:
            return
        self.last_name.setText(data["last_name"])
        self.first_name.setText(data["first_name"])
        self.middle_name.setText(data["middle_name"])
        self.marital_status.setText(data["marital_status"])
        self.gender.setText(data["gender"])
        self.dob.setText(data["dob"])
        self.birth_place.setText(data["place_of_birth"])
        self.address.setText(data["address"])
        self.contact_no.setText(data["contact_no"])
        self.email.setText(data["email"])
        self.sss_no.setText(data["sss_no"])
        self.tin_no.setText(data["tin_no"])
        self.position.setText(data["position"])
        self.hire_date.setText(data["hire_date"])
        self.pagibig_no.setText(data["pagibig_no"])
        self.philhealth_no.setText(data["philhealth_no"])
        self.salary.setText(f"₱{data['salary']:.2f}")

        img = data.get("profile_image")
        if img and os.path.isfile(img):
            pix = QPixmap(img)
            if not pix.isNull():
                self.picture_label.setPixmap(pix.scaled(
                    self.picture_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                ))
                
    def load_stylesheet(self):
        qss_path = os.path.join(os.path.dirname(__file__), "..", "styles", "personal_info_emp.qss")
        try:
            with open(os.path.abspath(qss_path), "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: attendance_admin.qss not found. Using default style.")
