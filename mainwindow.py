from PyQt4 import QtCore
from PyQt4 import QtGui
from point import Ui_MainWindow
import simplejson
import sys, Image, os
import numpy as np

class DesignerMainWindow(QtGui.QMainWindow, Ui_MainWindow):

  def __init__(self, parent=None):
    super(DesignerMainWindow, self).__init__(parent)
    self.setupUi(self)
    self.pointsOut = {}
    self.parseConfig()

    QtCore.QObject.connect(self.actionOpen, QtCore.SIGNAL("triggered()"), self.parseConfig)
    QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT("quit()"))
    QtCore.QObject.connect(self.pointsCombo, QtCore.SIGNAL("valueChanged(int)"), self.selectPoint)
    QtCore.QObject.connect(self.image1combo, QtCore.SIGNAL("currentIndexChanged(int)"), self.changeImage1)
    QtCore.QObject.connect(self.image2combo, QtCore.SIGNAL("currentIndexChanged(int)"), self.changeImage2)
    self.im1.canvas.mpl_connect('pick_event', self.onpick)
    self.im2.canvas.mpl_connect('pick_event', self.onpick)
    

  def onpick(self, event):
    if (event.artist.get_axes() == self.im1.axes):
      im = self.im1
      image  = self.image1combo.currentIndex()
    else:
      im = self.im2
      image  = self.image2combo.currentIndex()      
    x,y = event.artist.get_xdata()[0],event.artist.get_ydata()[0]    
    self.pointsOut[image][self.workingPoint] =   (x,y)
    self.plotPoints(im, image)
    

  def selectPoint(self, event):
    self.workingPoint = self.pointsCombo.value()
  
  def changeImage1(self, event):    
    self.im1.axes.lines = []
    self.im1fig = self.image1combo.currentIndex()
    print self.im1fig
    self.image1 = np.asarray(Image.open(self.params['root_directory'] + '/frames/' + self.params['filename_format']%int(self.im1fig)))
    self.im1.axes.imshow(self.image1)
    self.plotPoints(self.im1,self.im1fig)

  def changeImage2(self, event):
    self.im2.axes.lines = []
    self.im2fig = self.image2combo.currentIndex()
    print self.im1fig
    self.image2 = np.asarray(Image.open(self.params['root_directory'] + '/frames/' + self.params['filename_format']%int(self.im2fig)))
    self.im2.axes.imshow(self.image2)
    self.plotPoints(self.im2,self.im2fig)
    
  
  def parseConfig(self):
    configFile = str(QtGui.QFileDialog.getOpenFileName())
    self.params = simplejson.load(open(configFile))       
    self.points = np.load(self.params['npy'])   
    self.im1fig = 0
    self.im2fig = 0   
    self.workingPoint = 0
    self.image1 = np.asarray(Image.open(self.params['root_directory'] + '/frames/' + self.params['filename_format']%int(self.im1fig)))
    self.image2 = np.asarray(Image.open(self.params['root_directory'] + '/frames/' + self.params['filename_format']%int(self.im2fig)))
    self.populateCombos()
    self.drawImages()
    self.plotPoints(self.im1, self.im1fig)
    self.plotPoints(self.im2, self.im2fig)

  def drawImages(self):
    self.im1.axes.imshow(self.image1)
    self.im2.axes.imshow(self.image1)
    
  def populateCombos(self):
    number = len(os.listdir(self.params['root_directory'] + '/frames/'))    
    for i in range(number):
      self.image1combo.addItem(str(i))
      self.image2combo.addItem(str(i))
    self.pointsCombo.setMinimum(0)
    self.pointsCombo.setMaximum(len(self.points[0][0]))
    self.pointsCombo.setValue(0)
    for i in range(len(self.points[0][0])):      
      self.pointsOut[i] = {}
    
  def plotPoints(self, im, number):     
    #check if pointsOut have points for that image.
    im.axes.clear()
    self.drawImages()
    if (len(self.pointsOut[number]) != 0):
      # iterate the points
      for point in range(len(self.points[number][0])):
          x,y = self.points[number][0][point], self.points[number][1][point]
          lkey = [key for key, value in self.pointsOut[number].iteritems() if value == (x,y)]
          if (len(lkey) == 0):
            im.axes.plot(x,y, 'o', color = 'b', picker=3)
          else:
            # It's a classified point
            if (lkey[0] == self.pointsCombo.value()):
              im.axes.plot(x,y, 'd', color = 'm', picker=3)
            else:
              im.axes.plot(x,y, 'd', color = 'y', picker=3)
          
    else:
      #plot everything
      for point in range(len(self.points[number][0])):      
        im.axes.plot(self.points[number][0][point],self.points[number][1][point], 'o', color = 'b', picker=3)                    
    im.canvas.draw()
    

if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  dmw = DesignerMainWindow()
  dmw.show()
  sys.exit(app.exec_())