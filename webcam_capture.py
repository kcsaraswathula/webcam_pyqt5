# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 03:27:16 2022

@author: krishna
"""
import cv2
import sys
from PyQt5.QtWidgets import QApplication,QWidget,QDialog,QPushButton,QGraphicsView,QGraphicsScene \
     ,QGraphicsPixmapItem,QLabel
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import numpy as np
class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        self.cam_running=True
        self.cap = cv2.VideoCapture(0)
        while self.cam_running:
            ret, frame = self.cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(600, 500, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
        self.cap.release()       
    def stop_streaming(self):
        self.cam_running=False
        self.quit()                 
class UI(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("C:/Users/krishna/Downloads/OpenCV projects/video_capture.ui",self)
        self.setGeometry(100,100,800,600)
        livestream=self.findChild(QPushButton,'liveStream')
        livestream.clicked.connect(self.start_live_capture)
        stopcamera=self.findChild(QPushButton,'stopCamera')
        stopcamera.clicked.connect(self.stop_camera)    
        exitapp=self.findChild(QPushButton,'closeApp')
        exitapp.clicked.connect(self.exit_app) 
        self.label=self.findChild(QLabel,'label')
        self.label.setText("")
        self.label.resize(600,500)
        self.graphWidget=self.findChild(PlotWidget,'widget')
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]
        pen = pg.mkPen(color=(255, 0, 0))
        self.graphWidget.plot(hour, temperature, pen=pen)
        self.graphWidget.setBackground('w')
        styles = {'color':'w', 'font-size':'40px'}
        self.graphWidget.setLabel('left', 'Temperature (°C)', **styles)
        self.graphWidget.setLabel('bottom', 'Hour (H)', **styles)

    @pyqtSlot(QImage)  
    def show_image(self,image):
        self.label.setPixmap(QPixmap.fromImage(image))
    def start_live_capture(self):
        self.worker = Thread()
        self.worker.start()
        self.worker.changePixmap.connect(self.show_image)

    def stop_camera(self):

        self.worker.stop_streaming()
    def exit_app(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())             