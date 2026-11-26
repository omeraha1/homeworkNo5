import os
import sys
import subprocess
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget


class GraphWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setupUI()

        self.draw_btn.clicked.connect(self.draw_graph)
        self.clear_btn.clicked.connect(self.clear_graph)
        self.export_btn.clicked.connect(self.export_csv)

    def setupUI(self):
        self.setWindowTitle("Graph Window")
        self.resize(680, 420)

        layout = QHBoxLayout(self)

        self.fig = Figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
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


    def draw_graph(self):
        time_list = self.main_window.time_history
        temp1_list = self.main_window.body1_temp_history
        temp2_list = self.main_window.body2_temp_history

        if len(time_list) == 0:
            return

        choice = self.body_select.currentText()

        if choice == "Body 1":
            self.ax.plot(time_list, temp1_list, color="red", label="Body 1")
        elif choice == "Body 2":
            self.ax.plot(time_list, temp2_list, color="blue", label="Body 2")
        else:
            self.ax.plot(time_list, temp1_list, color="red", label="Body 1")
            self.ax.plot(time_list, temp2_list, color="blue", label="Body 2")

        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.legend()
        self.canvas.draw()

    def clear_graph(self):
        self.ax.clear()
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.canvas.draw()

    def export_csv(self):
        time_list = self.main_window.time_history
        temp1_list = self.main_window.body1_temp_history
        temp2_list = self.main_window.body2_temp_history

        if len(time_list) == 0:
            return

        file_name = "heat_transfer_data.csv"
        with open(file_name, "w") as f:
            f.write("Time (s),Body 1 Temp (C),Body 2 Temp (C)\n")
            for i in range(len(time_list)):
                f.write(f"{time_list[i]:.2f},{temp1_list[i]:.2f},{temp2_list[i]:.2f}\n")

        file_name = "heat_transfer_data.csv"
        with open(file_name, "w") as f:
            f.write("Time (s),Body 1 Temp (C),Body 2 Temp (C)\n")
            for i in range(len(time_list)):
                f.write(f"{time_list[i]:.2f},{temp1_list[i]:.2f},{temp2_list[i]:.2f}\n")

        if sys.platform.startswith("win"):
            os.startfile(file_name)
        elif sys.platform == "darwin":
            subprocess.run(["open", file_name])
        else:
            subprocess.run(["xdg-open", file_name])