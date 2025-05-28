from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from GUI.GridScene import *
from Components.AndGate import AndGate

class LeftDock(QDockWidget):
    def __init__(self, parent=None, scene=None, view=None):
        super().__init__("Components", parent)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setMinimumWidth(150)
        self.scene = scene
        self.view = view
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        # Shape buttons
        self.and_button = QPushButton("And")

        self.layout.addWidget(self.and_button)
        self.layout.addStretch()
        self.main_widget.setLayout(self.layout)
        self.setWidget(self.main_widget)

        # Connect buttons
        self.and_button.clicked.connect(lambda: self.add_shape("and"))

    def add_shape(self, shape_type):
        if not self.scene:
            return

        shape_map = {
            "and": (AndGate, (100, 50)),
        }

        if shape_type in shape_map:
            shape_class, args = shape_map[shape_type]
            item = shape_class(0, 0)
            item.setPos(100, 50) 
            self.scene.addItem(item)
            item.setSelected(True)