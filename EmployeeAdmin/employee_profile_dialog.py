from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QGridLayout, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
import os


class EmployeeProfileDialog(QDialog):
    def __init__(self, employee_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Employee Profile")
        self.setMinimumWidth(400)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Profile Picture - Circular and Centered
        pic_label = QLabel()
        pic_label.setFixedSize(120, 120)
        pic_label.setStyleSheet("border-radius: 60px; background-color: #ccc;")
        profile_image = employee_data.get("profile_image", None)
        if profile_image and os.path.exists(profile_image):
            pixmap = QPixmap(profile_image).scaled(120, 120, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

            # Circular mask
            mask = QPixmap(120, 120)
            mask.fill(Qt.transparent)

            from PySide6.QtGui import QPainter, QPainterPath
            painter = QPainter(mask)
            painter.setRenderHint(QPainter.Antialiasing)
            path = QPainterPath()
            path.addEllipse(0, 0, 120, 120)
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, pixmap)
            painter.end()

            pic_label.setPixmap(mask)
        else:
            pic_label.setText("🖼️")
            pic_label.setAlignment(Qt.AlignCenter)
            pic_label.setStyleSheet("font-size: 48px;")

        main_layout.addWidget(pic_label, alignment=Qt.AlignHCenter)

        # Full Name - Larger, Bold, Centered
        full_name = f"{employee_data.get('first_name', '')} "
        middle = employee_data.get('middle_name', '')
        if middle:
            full_name += f"{middle[0]}. "
        full_name += employee_data.get('last_name', '')

        name_label = QLabel(full_name.strip())
        name_label.setAlignment(Qt.AlignHCenter)
        name_label.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(name_label)

        # Employee ID - smaller, centered
        employee_id_label = QLabel(employee_data.get("employee_id", ""))
        employee_id_label.setAlignment(Qt.AlignHCenter)
        employee_id_label.setFont(QFont("Arial", 11))
        employee_id_label.setStyleSheet("color: gray;")
        main_layout.addWidget(employee_id_label)

        # Grid for other info: 2 columns
        info_grid = QGridLayout()
        info_grid.setSpacing(15)
        info_grid.setColumnMinimumWidth(0, 150)
        info_grid.setColumnMinimumWidth(1, 150)

        def make_label(text):
            lbl = QLabel(text)
            lbl.setFont(QFont("Arial", 10))
            return lbl

        # Left column
        info_grid.addWidget(make_label(f"Marital Status: {employee_data.get('marital_status', '')}"), 0, 0)
        info_grid.addWidget(make_label(f"Gender: {employee_data.get('gender', '')}"), 1, 0)
        info_grid.addWidget(make_label(f"Address: {employee_data.get('address', '')}"), 2, 0)
        info_grid.addWidget(make_label(f"Email: {employee_data.get('email', '')}"), 3, 0)
        info_grid.addWidget(make_label(f"SSS No: {employee_data.get('sss_no', '')}"), 4, 0)
        info_grid.addWidget(make_label(f"TIN No: {employee_data.get('tin_no', '')}"), 5, 0)
        info_grid.addWidget(make_label(f"Position: {employee_data.get('position', '')}"), 6, 0)

        # Right column
        info_grid.addWidget(make_label(f"Date of Birth: {employee_data.get('dob', '')}"), 0, 1)
        info_grid.addWidget(make_label(f"Place of Birth: {employee_data.get('place_of_birth', '')}"), 1, 1)
        info_grid.addWidget(make_label(f"Contact No: {employee_data.get('contact_no', '')}"), 2, 1)
        info_grid.addWidget(make_label(f"Pag-IBIG: {employee_data.get('pagibig_no', '')}"), 3, 1)
        info_grid.addWidget(make_label(f"PhilHealth: {employee_data.get('philhealth_no', '')}"), 4, 1)
        info_grid.addWidget(make_label(f"Hire Date: {employee_data.get('hire_date', '')}"), 5, 1)
        # Salary - formatted with currency symbol
        salary = employee_data.get('salary', 0)
        try:
            salary = float(salary)
        except (ValueError, TypeError):
            salary = 0.0  # fallback kung hindi valid number

        info_grid.addWidget(make_label(f"Salary: ₱{salary:,.2f}"), 6, 1)


        # Email & Place of Birth spanning full width below grid
        email_label = make_label(f"Email: {employee_data.get('email', '')}")
        

        main_layout.addLayout(info_grid)



        # Spacer
        main_layout.addStretch()

        # Close button centered
        close_btn = QPushButton("Close")
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(self.accept)
        main_layout.addWidget(close_btn, alignment=Qt.AlignHCenter)
