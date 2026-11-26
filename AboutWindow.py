from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("About")
        self.resize(380, 460)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(10)

        title = QLabel("Heat Transfer Simulator")
        title_font = QFont(title.font())
        title_font.setPointSize(19)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        photo = QLabel()
        photo.setFixedSize(190, 190)
        photo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        photo.setStyleSheet(
            "border: 1px solid #d1d5db; border-radius: 8px; background: #ffffff;"
        )
        image_path = Path(__file__).with_name("myphoto.png")
        pixmap = QPixmap(str(image_path))
        photo.setPixmap(
            pixmap.scaled(
                180,
                180,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

        name = QLabel("Omer Aharon")
        name_font = QFont(name.font())
        name_font.setBold(True)
        name.setFont(name_font)
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        email = QLabel("aharonomer3@gmail.com")
        email.setAlignment(Qt.AlignmentFlag.AlignCenter)

        github = QLabel(
            '<a href="https://github.com/omeraha1/homeworkNo5" '
            'style="color: #1d4ed8;">'
            "GitHub Project Repository</a>"
        )
        github.setOpenExternalLinks(True)
        github.setAlignment(Qt.AlignmentFlag.AlignCenter)

        linkedin = QLabel(
            '<a href="https://www.linkedin.com/in/omer-aharon-613698374/" '
            'style="color: #1d4ed8;">'
            "My LinkedIn Profile</a>"
        )
        linkedin.setOpenExternalLinks(True)
        linkedin.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.hide)

        layout.addWidget(title)
        layout.addWidget(photo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name)
        layout.addWidget(email)
        layout.addWidget(github)
        layout.addWidget(linkedin)
        layout.addStretch()
        layout.addWidget(self.close_btn)
