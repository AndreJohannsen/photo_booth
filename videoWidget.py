#!/usr/bin/python

# coding=utf8

# Original Code form:
# Copyright (C) 2011 Saul Ibarra Corretge <saghul@gmail.com>
#
# Some inspiration taken from: http://www.morethantechnical.com/2009/03/05/qt-opencv-combined-for-face-detecting-qwidgets/

import cv2
import cv2.cv as cv
import sys
import numpy as np
import os
import time

from PyQt4 import QtGui, QtCore

class IplQImage(QtGui.QImage):
        
    def __init__(self,iplimage):
        # Rough-n-ready but it works dammit
        # alpha = cv.CreateMat(iplimage.height,iplimage.width, cv.CV_8UC1)
        alpha = np.zeros((iplimage.shape[0],iplimage.shape[1]), np.uint8)
        # Zieht ein schwarzes Rechteck ueber das Bild
        cv2.rectangle(alpha, (0, 0), (iplimage.shape[1],iplimage.shape[0]),
                     cv.ScalarAll(255) ,-1)
        rgba = np.zeros((iplimage.shape[0], iplimage.shape[1], 4), np.uint8)
        #cv2.Set(rgba, (1, 2, 3, 4))
        cv2.mixChannels([iplimage, alpha],[rgba], [
        0, 0, # rgba[0] -> bgr[2]
        1, 1, # rgba[1] -> bgr[1]
        2, 2, # rgba[2] -> bgr[0]
        3, 3  # rgba[3] -> alpha[0]
        ])
        self.__imagedata = rgba.tostring()
        super(IplQImage,self).__init__(self.__imagedata, iplimage.shape[1],
                                       iplimage.shape[0], QtGui.QImage.Format_RGB32)


class VideoWidget(QtGui.QWidget):
    """ A class for rendering video coming from OpenCV """

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self._capture = cv2.VideoCapture(0)
        # Take one frame to query height
        rval, frame = self._capture.read()
        self._frame = None
        self._image = self._build_image(rval, frame)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.queryFrame)
        self._timer.start(50)
        self.savePath = "/home/jn/Dokumente/python/opencv/photo_booth/pics"
        self.screenTimerCount = 0
        self.currentDir = self.savePath

        
    def _build_image(self,rval, frame):
        if not rval:
            self._frame = np.zeros((frame.shape[0], frame.shape[1]),
                                   np.uint8, frame.shape[1])
        self._frame = frame
        return IplQImage(self._frame)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(QtCore.QPoint(0, 0), self._image)

        
    def queryFrame(self):
        rval, frame = self._capture.read()
        self._image = self._build_image(rval, frame)
        self.update()

        
    def mkfolder(self):
        folderName = self.savePath + "/" + time.strftime("%Y-%m-%d--%H-%M-%S")
        os.mkdir(folderName)
        self.currentDir = folderName

        
    def getScreenshot(self):
        picName = "pic" + str(self.screenTimerCount) + ".png"
        cv2.imwrite(self.currentDir + "/" + picName, self._frame)
        print(picName + " gespeichert")
        
        self.screenTimerCount += 1
        if self.screenTimerCount == 3:
            self.screenTimer.stop()
        
    def screenTimer(self):
        self.mkfolder()
        self.screenTimer = QtCore.QTimer()
        self.screenTimer.timeout.connect(self.getScreenshot)
        self.screenTimer.start(2000)
        
        
    def 
