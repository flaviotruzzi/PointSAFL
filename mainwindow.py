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

    QtCore.QObject.connect(self.actionOpen, QtCore.SIGNAL("triggered()"), self.parseConfig)
    QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT("quit()"))

  def parseConfig(self):
    configFile = str(QtGui.QFileDialog.getOpenFileName())
    self.params = simplejson.load(open(configFile))
    self.im1fig = 1    
    imageFilename1 = self.params['root_directory'] + '/framesset/' + self.params['filename_format']%int(self.im1fig)      
    self.image1 = np.asarray(Image.open(imageFilename1))    
    self.populateCombos()
    self.drawImages()


  def drawImages(self):
    self.im1.imshow(self.image1)
    self.im2.imshow(self.image1)
    
  def populateCombos(self):
    number = len(self.image1combo.addItems(os.listdir(self.params['root_directory'] + '/framesset/')))    
    for i in range(number):
      self.image1combo.addItem(str(i))
      self.image2combo.addItem(str(i))
    

if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  dmw = DesignerMainWindow()
  dmw.show()
  sys.exit(app.exec_())