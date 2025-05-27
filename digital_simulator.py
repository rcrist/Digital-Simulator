# PyQt6 & system imports
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

# Custom class imports
from Components.And import AndGate

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Simulator")
        self.setGeometry(200, 100, 1200, 600)

        # Create the Scene
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 1000, 500)

        # Create the view
        self.view = QGraphicsView(self.scene, self)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.view.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setCentralWidget(self.view)

        self.comp = AndGate(100, 100, 50, 50)
        self.scene.addItem(self.comp)

# Application main entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())