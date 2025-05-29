# PyQt6 & system imports
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

# Importing custom QGraphicsItems here
from Components.Comp import Comp

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Simulator")
        self.setGeometry(200, 100, 1200, 600) # x, y, width, height

        # Create the Scene
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 1000, 500)

        # Create the view
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Ensure the canvas origin is at the top-left of the view
        self.view.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.view.centerOn(0, 0)

        # Example: Add a Comp instance to a QGraphicsScene
        comp = Comp()
        self.scene.addItem(comp)

# Application main entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())