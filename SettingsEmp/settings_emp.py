from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
import os

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("SettingsPage")
        self.load_stylesheet()
        self.init_ui()

    def load_stylesheet(self):
        try:
            qss_path = os.path.join(os.path.dirname(__file__), "..", "styles", "settings_emp.qss")
            print("Loading stylesheet from:", os.path.abspath(qss_path))
            with open(os.path.abspath(qss_path), "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: styles/settings_emp.qss not found.")

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(50, 30, 50, 320)  # Similar spacing to dashboard

        container = QFrame()
        container.setObjectName("SettingsContainer")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(30, 30, 30, 150)
        container_layout.setSpacing(20)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 160))
        container.setGraphicsEffect(shadow)

        title_label = QLabel("Settings")
        title_label.setObjectName("SettingsTitle")
        title_label.setAlignment(Qt.AlignCenter)

        # Sample settings content
        placeholder_label = QLabel("Settings options will be shown here.")
        placeholder_label.setAlignment(Qt.AlignCenter)

        container_layout.addWidget(title_label)
        container_layout.addWidget(placeholder_label)

        main_layout.addWidget(container)
