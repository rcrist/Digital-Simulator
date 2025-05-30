from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Components.AndGate import AndGate

class LeftDock(QDockWidget):
    def __init__(self, parent=None, scene=None):
        super().__init__("Components", parent)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setMinimumWidth(150)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | 
                         QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.setFloating(False)
        
        self.scene = scene
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        # Gate buttons
        self.and_button = QPushButton("And Gate")

        self.layout.addWidget(self.and_button)
        self.layout.addStretch()
        self.main_widget.setLayout(self.layout)
        self.setWidget(self.main_widget)

        # Connect buttons
        self.and_button.clicked.connect(lambda: self.add_component("and"))

    def add_component(self, component_type):
        if not self.scene:
            return

        component_map = {
            "and": (AndGate, ()),
        }

        if component_type in component_map:
            component_class, args = component_map[component_type]
            item = component_class(*args)
            self.scene.addItem(item)
            item.setSelected(True)