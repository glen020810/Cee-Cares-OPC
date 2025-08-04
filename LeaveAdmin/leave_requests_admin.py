# EmployeeAdmin/leave_requests_admin.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QHBoxLayout, QFrame, QGraphicsDropShadowEffect, QMessageBox,
    QToolButton, QMenu, QTabWidget, QDialog, QFormLayout, QDialogButtonBox, QWidget
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt
import os
import EmployeeAdmin.emp_admin_db as db
from functools import partial

from LeaveAdmin.leave_history import LeaveHistoryTab  # <-- ✅ Import here


class LeaveRequestsAdmin(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("LeaveRequestAdminPage")
        self.load_stylesheet()

        self.tab_widget = QTabWidget()
        self.request_tab = QWidget()
        self.leave_history_tab = LeaveHistoryTab()  # <-- ✅ Use imported class

        self.tab_widget.addTab(self.request_tab, "Leave")
        self.tab_widget.addTab(self.leave_history_tab, "History")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(50, 30, 50, 30)

        container = QFrame()
        container.setObjectName("LeaveContainer")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(30, 30, 30, 30)
        container_layout.setSpacing(30)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 160))
        container.setGraphicsEffect(shadow)

        container_layout.addWidget(self.tab_widget)
        outer_layout.addWidget(container)

        self.init_request_tab_ui()


    def init_request_tab_ui(self):
        layout = QVBoxLayout(self.request_tab)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(20, 30, 20, 20)
        layout.setSpacing(20)

        title_label = QLabel("Leave Requests")
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title_label)

        self.build_table(layout)
        self.refresh_table()


    def build_table(self, parent_layout):
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Employee", "Leave Type", "Payment", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        parent_layout.addWidget(self.table)

    # ... [keep the rest of the functions: refresh_table, confirm_action, update_status, load_stylesheet]


    def refresh_table(self):
        self.table.setRowCount(0)
        try:
            leave_data = db.get_pending_leave_requests()
            print(f"[DEBUG] Retrieved {len(leave_data)} leave requests.")
            for row_data in leave_data:
                request_id = row_data[0]
                employee_id = row_data[1]
                employee_name = f"{employee_id} - {row_data[2]} {row_data[3]}"  # 👈 ID + Name
                visible_data = [employee_name] + list(row_data[4:9])  # rest of the fields

                row = self.table.rowCount()
                self.table.insertRow(row)

                # Composite widget with ID and clickable name
                employee_widget = QWidget()
                hbox = QHBoxLayout(employee_widget)
                hbox.setContentsMargins(0, 0, 0, 0)
                hbox.setSpacing(2)

                # Employee ID
                id_label = QLabel(f"{employee_id} - ")
                hbox.addWidget(id_label)

                # Name as clickable button
                name_button = QPushButton(f"{row_data[2]} {row_data[3]}")
                name_button.setStyleSheet("""
                    QPushButton {
                        color: #2a75f3;
                        background: transparent;
                        border: none;
                        text-decoration: underline;
                    }
                    QPushButton:hover {
                        color: #1a53d8;
                    }
                """)
                name_button.clicked.connect(partial(self.show_leave_details, row_data[6], row_data[7], row_data[8]))
                hbox.addWidget(name_button)

                self.table.setCellWidget(row, 0, employee_widget)


                # Leave Type and Payment
                self.table.setItem(row, 1, QTableWidgetItem(str(row_data[7])))  # Leave Type
                self.table.setItem(row, 2, QTableWidgetItem(str(row_data[8])))  # Payment

                # Action menu
                action_button = QToolButton()
                action_button.setText("⋮")
                action_button.setFocusPolicy(Qt.NoFocus)  # Prevents accidental focus grabbing
                action_button.setFixedSize(30, 30)
                action_button.setStyleSheet("QToolButton { font-size: 18px; padding: 0px; }")

                menu = QMenu()
                menu.addAction("✅ Approve", partial(self.update_status, request_id, "Approved"))
                menu.addAction("❌ Reject", partial(self.update_status, request_id, "Rejected"))

                def make_show_menu(btn, m):
                    return lambda: m.exec(btn.mapToGlobal(btn.rect().bottomLeft()))

                action_button.clicked.connect(make_show_menu(action_button, menu))
                self.table.setCellWidget(row, 3, action_button)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load leave requests:\n{e}")

    def confirm_action(self, request_id, status):
        action_text = "approve" if status == "Approved" else "reject"
        reply = QMessageBox.question(
            self,
            "Confirm Action",
            f"Are you sure you want to {action_text} this leave request?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.update_status(request_id, status)

    def update_status(self, request_id, status):
        try:
            db.update_leave_status(request_id, status, reviewed_by="Admin")
            QMessageBox.information(self, "Success", f"Leave request marked as {status}.")
            self.refresh_table()
            self.leave_history_tab.load_leave_history()  # Refresh history tab too!
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update leave status:\n{e}")

    def show_leave_details(self, start_date, end_date, reason):
        dialog = QDialog(self)
        dialog.setWindowTitle("Leave Details")
        dialog.resize(400, 200)
        layout = QFormLayout(dialog)

        layout.addRow("Start Date:", QLabel(str(start_date)))
        layout.addRow("End Date:", QLabel(str(end_date)))
        layout.addRow("Reason:", QLabel(str(reason)))

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)

        dialog.exec()

    def load_stylesheet(self):
        try:
            qss_path = os.path.join(os.path.dirname(__file__), "..", "styles", "leave_requests_admin.qss")
            with open(os.path.abspath(qss_path), "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: styles/leave_requests_admin.qss not found.")