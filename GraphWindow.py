from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget


class GraphWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Graph Window")
        self.resize(680, 420)

        layout = QHBoxLayout(self)

        self.fig = Figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")

        controls = QVBoxLayout()
        self.body_select = QComboBox()
        self.body_select.addItems(["Body 1", "Body 2", "Both"])
        self.draw_btn = QPushButton("Draw")
        self.clear_btn = QPushButton("Clear")
        self.export_btn = QPushButton("Export to CSV")

        controls.addWidget(self.body_select)
        controls.addWidget(self.draw_btn)
        controls.addWidget(self.clear_btn)
        controls.addWidget(self.export_btn)
        controls.addStretch()

        layout.addWidget(self.canvas, stretch=1)
        layout.addLayout(controls)
