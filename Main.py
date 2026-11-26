import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
    QAbstractSpinBox,
)


class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Heat Transfer")
        self.resize(900, 600)
        self.setMinimumSize(760, 500)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(24)

        top_layout = QGridLayout()
        top_layout.setColumnStretch(0, 4)
        top_layout.setColumnStretch(1, 3)
        top_layout.setColumnStretch(2, 4)
        top_layout.setHorizontalSpacing(0)
        top_layout.setVerticalSpacing(18)

        self.slider1 = QSlider(Qt.Orientation.Vertical)
        self.slider1.setRange(0, 200)
        self.slider1.setValue(200)

        self.body1 = QFrame()
        self.body1.setObjectName("body1")
        self.body1.setMinimumSize(110, 190)
        body1_layout = QVBoxLayout()
        body1_layout.setContentsMargins(0, 0, 0, 0)
        body1_layout.addWidget(QLabel("Body 1"), alignment=Qt.AlignmentFlag.AlignHCenter)
        body1_layout.addWidget(self.body1, stretch=1)

        left_layout = QHBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.slider1)
        left_layout.addLayout(body1_layout, stretch=1)

        cond_label = QLabel("Conductivity")
        cond_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cond = QDoubleSpinBox()
        self.cond.setSuffix(" J/s°C")
        self.cond.setDecimals(2)
        self.cond.setRange(0.01, 100.0)
        self.cond.setValue(1.00)

        connector = QFrame()
        connector.setObjectName("connector")
        connector.setFixedHeight(28)

        middle_layout = QVBoxLayout()
        middle_layout.setContentsMargins(0, 0, 0, 0)
        middle_layout.addWidget(cond_label)
        middle_layout.addWidget(self.cond)
        middle_layout.addStretch()
        middle_layout.addWidget(connector)
        middle_layout.addStretch()

        self.body2 = QFrame()
        self.body2.setObjectName("body2")
        self.body2.setMinimumSize(110, 190)
        body2_layout = QVBoxLayout()
        body2_layout.setContentsMargins(0, 0, 0, 0)
        body2_layout.addWidget(QLabel("Body 2"), alignment=Qt.AlignmentFlag.AlignHCenter)
        body2_layout.addWidget(self.body2, stretch=1)

        self.slider2 = QSlider(Qt.Orientation.Vertical)
        self.slider2.setRange(0, 200)
        self.slider2.setValue(0)

        right_layout = QHBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addLayout(body2_layout, stretch=1)
        right_layout.addWidget(self.slider2)

        top_layout.addLayout(left_layout, 0, 0)
        top_layout.addLayout(middle_layout, 0, 1)
        top_layout.addLayout(right_layout, 0, 2)

        bottom_layout = QGridLayout()
        bottom_layout.setColumnStretch(0, 4)
        bottom_layout.setColumnStretch(1, 2)
        bottom_layout.setColumnStretch(2, 4)
        bottom_layout.setHorizontalSpacing(28)
        bottom_layout.setVerticalSpacing(12)
        left_fields = QGridLayout()
        right_fields = QGridLayout()

        self.temp1 = QDoubleSpinBox()
        self.temp1.setReadOnly(True)
        self.temp1.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.temp1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.temp1.setSuffix(" °C")
        self.temp1.setDecimals(1)
        self.temp1.setRange(0, 200)
        self.temp1.setValue(200.0)

        self.mass1 = QDoubleSpinBox()
        self.mass1.setSuffix(" kg")
        self.mass1.setDecimals(2)
        self.mass1.setRange(0.01, 1000)
        self.mass1.setValue(10.00)

        self.hcap1 = QDoubleSpinBox()
        self.hcap1.setSuffix(" J/kg°C")
        self.hcap1.setDecimals(2)
        self.hcap1.setRange(0.01, 100)
        self.hcap1.setValue(0.40)

        for row, (label, spinbox) in enumerate(
            (("Temp.", self.temp1), ("Mass", self.mass1), ("H. Cap.", self.hcap1))
        ):
            left_fields.addWidget(QLabel(label), row, 0)
            left_fields.addWidget(spinbox, row, 1)
        left_fields.setColumnStretch(0, 1)
        left_fields.setColumnStretch(1, 3)

        buttons_layout = QVBoxLayout()
        self.start_btn = QPushButton("Start")
        self.start_btn.setObjectName("start_btn")
        self.start_btn.setCheckable(True)
        self.graph_btn = QPushButton("Graphs")
        self.about_btn = QPushButton("About")
        buttons_layout.addWidget(self.start_btn)
        buttons_layout.addWidget(self.graph_btn)
        buttons_layout.addSpacing(8)
        buttons_layout.addWidget(self.about_btn)
        buttons_layout.addStretch()

        self.temp2 = QDoubleSpinBox()
        self.temp2.setReadOnly(True)
        self.temp2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.temp2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.temp2.setSuffix(" °C")
        self.temp2.setDecimals(1)
        self.temp2.setRange(0, 200)
        self.temp2.setValue(0.0)

        self.mass2 = QDoubleSpinBox()
        self.mass2.setSuffix(" kg")
        self.mass2.setDecimals(2)
        self.mass2.setRange(0.01, 1000)
        self.mass2.setValue(10.00)

        self.hcap2 = QDoubleSpinBox()
        self.hcap2.setSuffix(" J/kg°C")
        self.hcap2.setDecimals(2)
        self.hcap2.setRange(0.01, 100)
        self.hcap2.setValue(0.40)

        for row, (spinbox, label) in enumerate(
            ((self.temp2, "Temp."), (self.mass2, "Mass"), (self.hcap2, "H. Cap."))
        ):
            right_fields.addWidget(spinbox, row, 0)
            right_fields.addWidget(QLabel(label), row, 1)
        right_fields.setColumnStretch(0, 3)
        right_fields.setColumnStretch(1, 1)

        bottom_layout.addLayout(left_fields, 0, 0)
        bottom_layout.addLayout(buttons_layout, 0, 1)
        bottom_layout.addLayout(right_fields, 0, 2)

        main_layout.addLayout(top_layout, stretch=3)
        main_layout.addLayout(bottom_layout, stretch=2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_path = Path(__file__).with_name("style.qss")
    app.setStyleSheet(style_path.read_text(encoding="utf-8"))
    window = HeatTransfer()
    window.show()
    sys.exit(app.exec())
