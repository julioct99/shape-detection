import sys
from PyQt5.QtWidgets import (
    QLineEdit, QSlider, QPushButton, QVBoxLayout, QApplication, QWidget, QLabel)
from PyQt5.QtCore import Qt


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def slider_change(self):
        self.label.setText(str(self.slider.value()))

    def init_ui(self):

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(99)
        self.slider.setValue(1)
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.slider_change)

        # Label
        self.label = QLabel()
        self.label.setText(str(self.slider.value()))

        v_box = QVBoxLayout()
        v_box.addWidget(self.label)
        v_box.addWidget(self.slider)

        self.setLayout(v_box)
        self.setWindowTitle('QT Widgets')

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a_window = Window()
    sys.exit(app.exec_())
