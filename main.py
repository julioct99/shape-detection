# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import QApplication
import cv2
import numpy as np
import image_process as mcv2
# definir numero total de imagenes a mostrar
MAX_IMG = 4

class Webcam:
    def __init__(self):
        # Cargamos la GUI desde el archivo UI.
        self.MAX_img = MAX_IMG
        self.cv_video = []
        self.MainWindow = uic.loadUi('webcam.ui')
        self.MainWindow.setWindowTitle("Shape Detection")
        self.qt_video=[self.MainWindow.video,self.MainWindow.video1,self.MainWindow.video2,self.MainWindow.video3]
        self.webcam = cv2.VideoCapture(0)
        blank_image = np.zeros((640,480,3), np.uint8)
        blue_image = np.zeros((640,480,3), np.uint8)
        blue_image[:] = (255, 0, 0)
        for i in range(MAX_IMG):
            self.cv_video.append(blue_image)

        self.MainWindow.canny_sup_slide.setRange(0,150)
        self.MainWindow.gauss_sigma_slide.setRange(0, 25)
        self.MainWindow.canny_inf_dial.setMaximum(150)
        self.MainWindow.canny_inf.setRange(0,150)
        self.MainWindow.canny_sup_slide.valueChanged.connect(self.change_canny_sup)
        self.MainWindow.gauss_sigma_slide.valueChanged.connect(self.change_sigma_value)
        self.MainWindow.canny_inf_dial.valueChanged.connect(self.change_canny_inf)

        self.timer_filter = QtCore.QTimer(self.MainWindow);
        self.timer_filter.timeout.connect(self.make_filter) #timer para los filtros de cv2 funcion que ejecuta
        self.timer_filter.start(3);

        self.timer_frames = QtCore.QTimer(self.MainWindow);
        self.timer_frames.timeout.connect(self.show_frames) #timer para refrescar la ventana
        self.timer_frames.start(3);

    def change_canny_inf(self):
        self.MainWindow.canny_inf.setValue(self.MainWindow.canny_inf_dial.value())

    def change_canny_sup(self):
        self.MainWindow.canny_sup.display(self.MainWindow.canny_sup_slide.value())

    def change_sigma_value(self):
        self.MainWindow.gauss_sigma_value.display(self.MainWindow.gauss_sigma_slide.value())


    def make_filter(self):
        font = cv2.FONT_HERSHEY_SIMPLEX
        ok,entrada = self.webcam.read()
        self.height, self.width = entrada.shape[:2]
        self.cv_video[0] = entrada.copy()
        self.cv_video[1] = cv2.GaussianBlur(entrada, (5,5), self.MainWindow.gauss_sigma_slide.value())
        self.cv_video[2] = cv2.cvtColor(entrada, cv2.COLOR_BGR2GRAY)
        self.cv_video[2] = cv2.Canny(self.cv_video[1], self.MainWindow.canny_inf.value(), self.MainWindow.canny_sup.value())
        self.cv_video[3] = mcv2.find_contorno(self.cv_video[2],entrada)

    def show_frames(self):
            for i in range(len(self.qt_video)):
                self.convertCV2ToQimage(self.cv_video[i],self.qt_video[i])

    def convertCV2ToQimage(self,cv_vid,qt_vid):
        gray_color_table = [QtGui.qRgb(i, i, i) for i in range(256)]
        if cv_vid is None:
            return
        if cv_vid.dtype != np.uint8:
            return
        if len(cv_vid.shape) == 2:
            image = QtGui.QImage(cv_vid, cv_vid.shape[1], cv_vid.shape[0], cv_vid.strides[0], QtGui.QImage.Format_Indexed8)
            image.setColorTable(gray_color_table)
        if len(cv_vid.shape) == 3:
            if cv_vid.shape[2] == 3:
               image = QtGui.QImage(cv_vid, cv_vid.shape[1], cv_vid.shape[0], cv_vid.strides[0], QtGui.QImage.Format_RGB888)
            elif cv_vid.shape[2] == 4:
               image = QtGui.QImage(cv_vid, cv_vid.shape[1], cv_vid.shape[0], cv_vid.strides[0], QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        qt_vid.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    webcam = Webcam()
    webcam.MainWindow.show()
    app.exec_()
