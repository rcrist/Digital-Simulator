# PyQt6 & system imports
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

# Custom class imports
from GUI.GridScene import GridScene
from GUI.ConfiguredView import ConfiguredView
from GUI.LeftDock import LeftDock

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Simulator")
        self.setGeometry(200, 100, 1200, 600)

        # Create the Scene
        self.scene = GridScene(self)
        self.scene.setSceneRect(0, 0, 1000, 500)

        # Create the view
        self.view = ConfiguredView(self.scene)
        self.setCentralWidget(self.view)

        # Left Dock (Shapes)
        self.left_dock = LeftDock(self, self.scene, self.view)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.left_dock)

# Application main entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())