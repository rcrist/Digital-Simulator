# PyQt6 & system imports
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

# Custom class imports
from GUI.GridScene import GridScene
from GUI.AppView import AppView
from GUI.TopMenu import TopMenu
from GUI.LeftDock import LeftDock
from GUI.RightDock import RightDock

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Simulator")
        self.setGeometry(200, 100, 1200, 600)

        # Create the Scene
        self.scene = GridScene(self)
        self.scene.setSceneRect(0, 0, 1000, 500)

        # Create the view
        self.view = AppView(self.scene)
        self.setCentralWidget(self.view)

        # Add MenuBar
        self.menu_bar = TopMenu(self, self.scene, self.view)
        self.setMenuBar(self.menu_bar)
        self.menu_bar.apply_dark_theme()

        # Ensure the canvas origin is at the top-left of the view
        self.view.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.view.centerOn(0, 0)

        # Left Dock (Shapes)
        self.left_dock = LeftDock(self, self.scene, self.view)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.left_dock)

        # Right Dock (Properties)
        self.right_dock = RightDock(self, self.scene, self.view)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.right_dock)

# Application main entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())