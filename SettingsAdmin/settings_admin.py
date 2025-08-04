from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel, QFrame, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from SettingsAdmin.server_settings import ServerSettingsPage  # Import natin yung bagong server settings page


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("SettingsPage")

        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(50, 30, 50, 30)

        # Container Frame for background
        container = QFrame()
        container.setObjectName("ContainerFrame")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)

        # Shadow Effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 160))
        container.setGraphicsEffect(shadow)

        # Tabs
        tabs = QTabWidget()
        tabs.setObjectName("SettingsTabs")

        # Details Tab
        details_tab = QWidget()
        details_layout = QVBoxLayout(details_tab)
        details_label = QLabel("Edit your account details here.")
        details_label.setAlignment(Qt.AlignCenter)
        details_layout.addWidget(details_label)
        tabs.addTab(details_tab, "Details")

        # Server Tab - gamit na yung ServerSettingsPage
        server_tab = ServerSettingsPage()
        tabs.addTab(server_tab, "Server")

        container_layout.addWidget(tabs)
        main_layout.addWidget(container)

        self.load_stylesheet()

    def load_stylesheet(self):
        try:
            with open("styles/settings.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Warning: styles/settings.qss not found. Default style applied.")
