# PyQt6 & system imports
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

# Importing custom QGraphicsItems here
from GUI.LeftDock import LeftDock
from GUI.RightDock import RightDock
from Components.Comp import Comp
from Components.AndGate import AndGate

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

        # Create the left dock with component buttons
        self.left_dock = LeftDock(self, self.scene)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.left_dock)

        # Create the right dock for properties
        self.right_dock = RightDock(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.right_dock)

        # Test new components here
        # comp = AndGate()
        # self.scene.addItem(comp)

        # Connect selection change to update properties panel
        self.scene.selectionChanged.connect(self.on_selection_changed)

    def on_selection_changed(self):
        selected_items = self.scene.selectedItems()
        if selected_items:
            self.right_dock.set_controls(selected_items[0])

# Application main entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())