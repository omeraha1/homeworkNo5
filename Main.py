import sys
from pathlib import Path

from PySide6.QtCore import Qt , QTimer
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
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
from Body import Body
from AboutWindow import AboutWindow
from GraphWindow import GraphWindow


class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()
        self.graph_window = GraphWindow(self)
        self.about_window = AboutWindow()

        self.bodyNo1 = None
        self.bodyNo2 = None
        self.dt = 0.1
        self.cnt_t = 0.0
        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_method)

        self.setupUI()

        self.mat1.currentTextChanged.connect(self.material1_changed)
        self.mat2.currentTextChanged.connect(self.material2_changed)
        self.slider1.valueChanged.connect(self.left_temperature_changed)
        self.slider2.valueChanged.connect(self.right_temperature_changed)
        self.start_btn.clicked.connect(self.start_stop_button_method)
        self.graph_btn.clicked.connect(self.show_graph)
        self.about_btn.clicked.connect(self.show_about)

        self.left_temperature_changed()
        self.right_temperature_changed()

    def show_graph(self):
        self.graph_window.show()

    def show_about(self):
        self.about_window.show()

    def closeEvent(self, event):
        self.graph_window.close()
        self.about_window.close()
        event.accept()

    def get_rgb(self, temp):
        if temp > 200:
            temp = 200
        if temp < 0:
            temp = 0
        red = int(temp * 255 / 200)
        green = int(150 - temp * 80 / 200)
        blue = int(255 - temp * 215 / 200)
        return red, green, blue

    def update_color(self, body_widget, temp):
        r, g, b = self.get_rgb(temp)
        body_widget.setStyleSheet(
            f"background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
            f"stop:0 rgb({r}, {g}, {b}), stop:1 rgb({max(0, r-35)}, {max(0, g-35)}, {max(0, b-35)})); "
            f"border-radius: 12px;"
        )

    def update_bridge(self):
        r1, g1, b1 = self.get_rgb(self.temp1.value())
        r2, g2, b2 = self.get_rgb(self.temp2.value())
        self.connector.setStyleSheet(
            f"background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 rgb({r1}, {g1}, {b1}), stop:1 rgb({r2}, {g2}, {b2})); "
            f"border-radius: 6px;"
        )

    def left_temperature_changed(self):
        t = self.slider1.value()
        self.temp1.setValue(t)
        self.update_color(self.body1, t)
        self.update_bridge()

    def right_temperature_changed(self):
        t = self.slider2.value()
        self.temp2.setValue(t)
        self.update_color(self.body2, t)
        self.update_bridge()

    def start_stop_button_method(self):
        if self.start_btn.isChecked():
            self.bodyNo1 = Body(self.mass1.value(), self.hcap1.value(), self.temp1.value())
            self.bodyNo2 = Body(self.mass2.value(), self.hcap2.value(), self.temp2.value())
            self.start_btn.setText("Stop")
            self.timer.start(100)
        else:
            self.timer.stop()
            self.start_btn.setText("Start")

    def start_stop_button_method(self):
        if self.start_btn.isChecked():
            self.bodyNo1 = Body(self.mass1.value(), self.hcap1.value(), self.temp1.value())
            self.bodyNo2 = Body(self.mass2.value(), self.hcap2.value(), self.temp2.value())

            self.cnt_t = 0.0
            self.time_history = [0.0]
            self.body1_temp_history = [self.bodyNo1.temperature]
            self.body2_temp_history = [self.bodyNo2.temperature]

            self.start_btn.setText("Stop")
            self.timer.start(100)
        else:
            self.timer.stop()
            self.start_btn.setText("Start")

    def timer_method(self):
        cond = self.cond.value()
        t1 = self.bodyNo1.temperature
        t2 = self.bodyNo2.temperature

        i1 = cond * (t2 - t1)
        i2 = cond * (t1 - t2)

        q1 = (i1 + self.watt1.value()) * self.dt
        q2 = (i2 + self.watt2.value()) * self.dt

        new_t1 = self.bodyNo1.add_heat(q1)
        new_t2 = self.bodyNo2.add_heat(q2)

        if new_t1 < 0:
            new_t1 = 0
            self.bodyNo1.temperature = 0
        if new_t2 < 0:
            new_t2 = 0
            self.bodyNo2.temperature = 0

        self.slider1.setValue(int(new_t1))
        self.slider2.setValue(int(new_t2))
        self.temp1.setValue(new_t1)
        self.temp2.setValue(new_t2)
        self.update_color(self.body1, new_t1)
        self.update_color(self.body2, new_t2)
        self.update_bridge()

        self.cnt_t += self.dt
        self.time_history.append(self.cnt_t)
        self.body1_temp_history.append(new_t1)
        self.body2_temp_history.append(new_t2)

        if self.auto_stop_cb.isChecked() and abs(new_t1 - new_t2) < 0.1:
            self.timer.stop()
            self.start_btn.setChecked(False)
            self.start_btn.setText("Start")

    def material1_changed(self):
        materials = {"Copper": 0.39, "Aluminum": 0.90, "Iron": 0.45, "Water": 4.18}
        name = self.mat1.currentText()
        if name in materials:
            self.hcap1.setValue(materials[name])

    def material2_changed(self):
        materials = {"Copper": 0.39, "Aluminum": 0.90, "Iron": 0.45, "Water": 4.18}
        name = self.mat2.currentText()
        if name in materials:
            self.hcap2.setValue(materials[name])


    def setupUI(self):
        self.setWindowTitle("Heat Transfer")
        self.setObjectName("heat_window")
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

        self.connector = QFrame()
        self.connector.setObjectName("connector")
        self.connector.setFixedHeight(28)

        middle_layout = QVBoxLayout()
        middle_layout.setContentsMargins(0, 0, 0, 0)
        middle_layout.addWidget(cond_label)
        middle_layout.addWidget(self.cond)
        middle_layout.addStretch()
        middle_layout.addWidget(self.connector)
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

        self.mat1 = QComboBox()
        self.mat1.addItems(["Custom", "Copper", "Aluminum", "Iron", "Water"])

        self.watt1 = QDoubleSpinBox()
        self.watt1.setRange(-500.0, 500.0)
        self.watt1.setDecimals(0)
        self.watt1.setValue(0)
        self.watt1.setSuffix(" W")

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

        for row, (label, control) in enumerate(
            (
                ("Material", self.mat1),
                ("Heater", self.watt1),
                ("Temp.", self.temp1),
                ("Mass", self.mass1),
                ("H. Cap.", self.hcap1),
            )
        ):
            left_fields.addWidget(QLabel(label), row, 0)
            left_fields.addWidget(control, row, 1)
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
        self.auto_stop_cb = QCheckBox("Auto-stop")
        self.auto_stop_cb.setChecked(True)
        buttons_layout.addWidget(self.auto_stop_cb)
        buttons_layout.addStretch()

        self.temp2 = QDoubleSpinBox()
        self.temp2.setReadOnly(True)
        self.temp2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.temp2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.temp2.setSuffix(" °C")
        self.temp2.setDecimals(1)
        self.temp2.setRange(0, 200)
        self.temp2.setValue(0.0)

        self.mat2 = QComboBox()
        self.mat2.addItems(["Custom", "Copper", "Aluminum", "Iron", "Water"])

        self.watt2 = QDoubleSpinBox()
        self.watt2.setRange(-500.0, 500.0)
        self.watt2.setDecimals(0)
        self.watt2.setValue(0)
        self.watt2.setSuffix(" W")

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

        for row, (control, label) in enumerate(
            (
                (self.mat2, "Material"),
                (self.watt2, "Heater"),
                (self.temp2, "Temp."),
                (self.mass2, "Mass"),
                (self.hcap2, "H. Cap."),
            )
        ):
            right_fields.addWidget(control, row, 0)
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
